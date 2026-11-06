
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from qa_platform.workload import submit_workload,wait_for_completion
url="http://127.0.0.1:8000"
normal=submit_workload(url,20,5); wait_for_completion(url,normal["job_ids"])
print("Normal phase done; starting 10x burst") 
burst=submit_workload(url,200,50)
states=wait_for_completion(url,burst["job_ids"],timeout_s=180)
print({"submitted":burst["submitted"],"completed":states.count("completed"),"failed":states.count("failed")})
