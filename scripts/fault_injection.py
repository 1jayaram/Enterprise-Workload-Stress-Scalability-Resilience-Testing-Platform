import httpx
from qa_platform.workload import wait_for_completion
url="http://127.0.0.1:8000"; ids=[]
for i in range(100):
    r=httpx.post(url+"/jobs",json={"name":f"fault-{i}","cpu":1,"memory_mb":64,
        "duration_s":0.2,"fail_probability":0.25})
    r.raise_for_status(); ids.append(r.json()["id"])
states=wait_for_completion(url,ids)
print({"completed":states.count("completed"),"failed":states.count("failed")})
