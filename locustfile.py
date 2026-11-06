from locust import HttpUser,task,between
class SchedulerUser(HttpUser):
    wait_time=between(0.1,0.5)
    @task(4)
    def submit_job(self):
        self.client.post("/jobs",json={"name":"locust-job","cpu":1,"memory_mb":64,
            "priority":1,"duration_s":0.2})
    @task(1)
    def cluster(self): self.client.get("/cluster")
    @task(1)
    def list_jobs(self): self.client.get("/jobs?limit=100")
