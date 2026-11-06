import json,sys,matplotlib.pyplot as plt
with open(sys.argv[1], encoding='utf-8-sig') as f: report=json.load(f)
m=report["submission_latency"]
labels=["Mean","P50","P95","P99","Max"]
values=[m["mean_ms"],m["p50_ms"],m["p95_ms"],m["p99_ms"],m["max_ms"]]
plt.figure(figsize=(8,5)); plt.bar(labels,values)
plt.ylabel("Latency (ms)"); plt.title("Scheduler API latency")
plt.tight_layout(); plt.savefig("reports/latency.png",dpi=150)
print("Saved reports/latency.png")
