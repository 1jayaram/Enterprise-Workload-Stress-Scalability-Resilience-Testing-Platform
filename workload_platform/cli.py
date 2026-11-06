import json, typer, httpx
cli=typer.Typer(help="Workload scheduler CLI")
BASE="http://127.0.0.1:8000"

@cli.command()
def submit(name:str,duration:float=1.0,cpu:int=1,memory:int=128,priority:int=0):
    p={"name":name,"duration_s":duration,"cpu":cpu,"memory_mb":memory,"priority":priority}
    r=httpx.post(f"{BASE}/jobs",json=p,timeout=10); r.raise_for_status()
    typer.echo(json.dumps(r.json(),indent=2))

@cli.command()
def jobs(status:str=""):
    r=httpx.get(f"{BASE}/jobs",params=({"status":status} if status else {}),timeout=10)
    r.raise_for_status(); typer.echo(json.dumps(r.json(),indent=2))

@cli.command()
def cluster():
    r=httpx.get(f"{BASE}/cluster",timeout=10); r.raise_for_status()
    typer.echo(json.dumps(r.json(),indent=2))

@cli.command()
def cancel(job_id:str):
    r=httpx.delete(f"{BASE}/jobs/{job_id}",timeout=10); r.raise_for_status()
    typer.echo(r.text)

if __name__=="__main__": cli()
