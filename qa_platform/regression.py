import json,sys

def compare(baseline_path,current_path,threshold=0.15):
    with open(baseline_path) as f: old=json.load(f)
    with open(current_path) as f: new=json.load(f)
    regressions=[]
    for metric in ("mean_ms","p95_ms","p99_ms"):
        before=old["submission_latency"].get(metric,0)
        after=new["submission_latency"].get(metric,0)
        if before>0 and after>before*(1+threshold):
            regressions.append({"metric":metric,"baseline":before,"current":after,
                "degradation_percent":(after/before-1)*100})
    return {"passed":not regressions,"threshold_percent":threshold*100,"regressions":regressions}

if __name__=="__main__":
    result=compare(sys.argv[1],sys.argv[2]); print(json.dumps(result,indent=2))
    sys.exit(0 if result["passed"] else 1)
