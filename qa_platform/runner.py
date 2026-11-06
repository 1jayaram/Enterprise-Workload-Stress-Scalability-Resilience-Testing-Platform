import argparse,json,os,time,httpx
from .workload import submit_workload,wait_for_completion
from .metrics import ProcessMonitor,summarize

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--url",default="http://127.0.0.1:8000")
    p.add_argument("--jobs",type=int,default=100)
    p.add_argument("--concurrency",type=int,default=10)
    p.add_argument("--duration",type=float,default=0.05)
    p.add_argument("--output",default="reports/latest.json")
    a=p.parse_args()
    pid=httpx.get(a.url+"/metrics/process",timeout=10).json()["pid"]
    monitor=ProcessMonitor(pid=pid); monitor.start(); start=time.perf_counter()
    result=submit_workload(a.url,a.jobs,a.concurrency,duration_s=a.duration)
    states=wait_for_completion(a.url,result["job_ids"])
    elapsed=time.perf_counter()-start; system=monitor.stop()
    completed=states.count("completed")
    report={"configuration":{"jobs":a.jobs,"concurrency":a.concurrency,"duration_s":a.duration},
      "elapsed_s":elapsed,"throughput_jobs_s":completed/elapsed if elapsed else 0,
      "submission_latency":summarize(result["latencies_ms"]),
      "terminal_states":{s:states.count(s) for s in set(states)},
      "process_monitor":system,"submission_errors":result["errors"]}
    os.makedirs(os.path.dirname(a.output) or ".",exist_ok=True)
    with open(a.output,"w") as f: json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
