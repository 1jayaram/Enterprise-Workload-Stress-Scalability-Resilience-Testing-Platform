from contextlib import asynccontextmanager
import os, psutil
from fastapi import FastAPI, HTTPException, Query
from . import database
from .models import JobCreate, JobOut
from .scheduler import Scheduler

scheduler = Scheduler()

@asynccontextmanager
async def lifespan(app):
    database.init_db()
    scheduler.recover_orphaned_jobs()
    scheduler.start()
    yield
    scheduler.stop()

app = FastAPI(title="Enterprise Workload Scheduler",version="1.0.0",lifespan=lifespan)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/jobs",response_model=JobOut,status_code=201)
def submit_job(job: JobCreate):
    try:
        return scheduler.submit(job.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422,detail=str(exc))

@app.get("/jobs",response_model=list[JobOut])
def list_jobs(status: str|None=Query(default=None),limit: int=Query(default=100,ge=1,le=1000)):
    if status and status not in {"queued","running","completed","failed","cancelled"}:
        raise HTTPException(status_code=400,detail="Invalid status filter")
    return scheduler.list_jobs(status,limit)

@app.get("/jobs/{job_id}",response_model=JobOut)
def get_job(job_id: str):
    job=scheduler.get_job(job_id)
    if not job: raise HTTPException(status_code=404,detail="Job not found")
    return job

@app.delete("/jobs/{job_id}")
def cancel_job(job_id: str):
    if scheduler.cancel(job_id): return {"cancelled":True,"job_id":job_id}
    job=scheduler.get_job(job_id)
    if not job: raise HTTPException(status_code=404,detail="Job not found")
    raise HTTPException(status_code=409,detail=f"Cannot cancel job in state {job['status']}")

@app.get("/cluster")
def cluster():
    return scheduler.cluster_status()

@app.get("/metrics/process")
def process_metrics():
    proc = psutil.Process(os.getpid())
    return {"pid": os.getpid(), "cpu_percent": proc.cpu_percent(None), "rss_mb": proc.memory_info().rss / 1048576}
