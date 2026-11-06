import os,time,threading,psutil

class ProcessMonitor:
    def __init__(self,interval=0.25,pid=None):
        self.proc=psutil.Process(pid or os.getpid()); self.interval=interval
        self.samples=[]; self.stop_event=threading.Event()
    def start(self):
        self.proc.cpu_percent(None)
        self.thread=threading.Thread(target=self._sample,daemon=True); self.thread.start()
    def _sample(self):
        while not self.stop_event.is_set():
            try:
                self.samples.append({"timestamp":time.time(),"cpu_percent":self.proc.cpu_percent(None),
                    "rss_mb":self.proc.memory_info().rss/1048576})
            except psutil.Error: break
            self.stop_event.wait(self.interval)
    def stop(self):
        self.stop_event.set(); self.thread.join(timeout=2); return self.summary()
    def summary(self):
        if not self.samples: return {"cpu_avg_percent":0,"memory_peak_mb":0,"samples":0}
        return {"cpu_avg_percent":sum(x["cpu_percent"] for x in self.samples)/len(self.samples),
                "memory_peak_mb":max(x["rss_mb"] for x in self.samples),"samples":len(self.samples)}

def percentile(values,p):
    if not values:return 0
    a=sorted(values); x=(len(a)-1)*p/100; lo=int(x); hi=min(lo+1,len(a)-1)
    return a[lo]+(a[hi]-a[lo])*(x-lo)

def summarize(values):
    return {"count":len(values),"mean_ms":sum(values)/len(values) if values else 0,
            "p50_ms":percentile(values,50),"p95_ms":percentile(values,95),
            "p99_ms":percentile(values,99),"max_ms":max(values,default=0)}
