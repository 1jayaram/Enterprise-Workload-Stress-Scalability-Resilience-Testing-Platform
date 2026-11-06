
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import argparse,time
from qa_platform.workload import submit_workload,wait_for_completion
p=argparse.ArgumentParser(); p.add_argument("--minutes",type=int,default=60)
p.add_argument("--batch",type=int,default=100); a=p.parse_args()
deadline=time.time()+a.minutes*60; rounds=0
while time.time()<deadline:
    result=submit_workload("http://127.0.0.1:8000",a.batch,10)
    wait_for_completion("http://127.0.0.1:8000",result["job_ids"],timeout_s=180)
    rounds+=1; print(f"Completed batch {rounds}")
print(f"Finished {rounds} batches")
