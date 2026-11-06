import random,time,httpx
from concurrent.futures import ThreadPoolExecutor,as_completed

def submit_workload(base_url,total_jobs=100,concurrency=10,seed=7,duration_s=0.05,fail_probability=0):
    random.seed(seed)
    payloads=[{"name":f"load-{i}","command":"benchmark","cpu":1,"memory_mb":64,
               "priority":random.randint(0,10),"duration_s":duration_s,
               "fail_probability":fail_probability} for i in range(total_jobs)]
    latencies,errors,ids=[],[],[]
    def send(p):
        start=time.perf_counter()
        try:
            r=httpx.post(f"{base_url}/jobs",json=p,timeout=15); elapsed=(time.perf_counter()-start)*1000
            r.raise_for_status(); return elapsed,r.json()["id"],None
        except Exception as e: return (time.perf_counter()-start)*1000,None,str(e)
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures=[pool.submit(send,p) for p in payloads]
        for f in as_completed(futures):
            latency,jid,error=f.result(); latencies.append(latency)
            if jid: ids.append(jid)
            if error: errors.append(error)
    return {"submitted":len(ids),"errors":len(errors),"latencies_ms":latencies,"job_ids":ids}

def wait_for_completion(base_url,job_ids,timeout_s=120,poll_s=0.25):
    deadline=time.time()+timeout_s
    terminal={"completed","failed","cancelled"}
    while time.time()<deadline:
        r=httpx.get(f"{base_url}/jobs",params={"limit":1000},timeout=10); r.raise_for_status()
        jobs={j["id"]:j for j in r.json()}
        states=[jobs.get(jid,{}).get("status") for jid in job_ids]
        if all(s in terminal for s in states): return states
        time.sleep(poll_s)
    raise TimeoutError("Timed out waiting for jobs")
