import random, threading, time, uuid
from concurrent.futures import ThreadPoolExecutor
from . import database
from .config import settings

class Scheduler:
    """In-process multi-worker simulator with CPU and memory admission control."""
    def __init__(self, workers=None, cpu_capacity=None, memory_capacity_mb=None):
        self.worker_count = workers or settings.workers
        self.cpu_capacity = cpu_capacity or settings.cpu_capacity
        self.memory_capacity_mb = memory_capacity_mb or settings.memory_mb
        self.pool = ThreadPoolExecutor(max_workers=self.worker_count)
        self.lock = threading.RLock()
        self.stop_event = threading.Event()
        self.dispatcher = None
        self.active = {}
        self.slots = {f"worker-{i+1}": None for i in range(self.worker_count)}
        self.used_cpu = 0
        self.used_memory = 0

    def start(self):
        database.init_db()
        with self.lock:
            if self.dispatcher and self.dispatcher.is_alive():
                return
            self.stop_event.clear()
            self.dispatcher = threading.Thread(target=self._loop, daemon=True)
            self.dispatcher.start()

    def stop(self):
        self.stop_event.set()
        if self.dispatcher:
            self.dispatcher.join(timeout=2)
        self.pool.shutdown(wait=False, cancel_futures=False)

    def submit(self, p):
        if p["cpu"] > self.cpu_capacity:
            raise ValueError("CPU request exceeds cluster capacity")
        if p["memory_mb"] > self.memory_capacity_mb:
            raise ValueError("Memory request exceeds cluster capacity")
        jid, now = str(uuid.uuid4()), time.time()
        with database.transaction() as con:
            con.execute("""INSERT INTO jobs
            (id,name,command,cpu,memory_mb,priority,duration_s,fail_probability,status,submitted_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (jid,p["name"],p["command"],p["cpu"],p["memory_mb"],p["priority"],
             p["duration_s"],p["fail_probability"],"queued",now))
        return self.get_job(jid)

    def get_job(self, jid):
        with database.connect() as con:
            row = con.execute("SELECT * FROM jobs WHERE id=?", (jid,)).fetchone()
        return dict(row) if row else None

    def list_jobs(self, status=None, limit=100):
        with database.connect() as con:
            if status:
                rows = con.execute("SELECT * FROM jobs WHERE status=? ORDER BY submitted_at DESC LIMIT ?",(status,limit)).fetchall()
            else:
                rows = con.execute("SELECT * FROM jobs ORDER BY submitted_at DESC LIMIT ?",(limit,)).fetchall()
        return [dict(r) for r in rows]

    def cancel(self, jid):
        with database.transaction() as con:
            cur = con.execute("UPDATE jobs SET status='cancelled',finished_at=? WHERE id=? AND status='queued'",(time.time(),jid))
        return cur.rowcount == 1

    def _loop(self):
        while not self.stop_event.is_set():
            self._dispatch()
            time.sleep(0.02)

    def _dispatch(self):
        with self.lock:
            free = [w for w,j in self.slots.items() if j is None]
            if not free:
                return
            with database.connect() as con:
                queue = con.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY priority DESC,submitted_at ASC").fetchall()
            for worker in free:
                job = next((j for j in queue if j["cpu"]+self.used_cpu <= self.cpu_capacity
                            and j["memory_mb"]+self.used_memory <= self.memory_capacity_mb),None)
                if job is None:
                    break
                jid = job["id"]
                self.slots[worker] = jid
                self.used_cpu += job["cpu"]
                self.used_memory += job["memory_mb"]
                with database.transaction() as con:
                    con.execute("UPDATE jobs SET status='running',worker_id=?,started_at=? WHERE id=? AND status='queued'",
                                (worker,time.time(),jid))
                self.active[jid] = (job["cpu"],job["memory_mb"],worker)
                self.pool.submit(self._execute,jid,worker,job["duration_s"],job["fail_probability"])

    def _execute(self,jid,worker,duration,fail_probability):
        status,error = "completed",None
        try:
            time.sleep(duration)
            if random.random() < fail_probability:
                raise RuntimeError("Injected simulated task failure")
        except Exception as exc:
            status,error = "failed",str(exc)
        finally:
            with self.lock:
                resources = self.active.pop(jid,None)
                if resources:
                    cpu,mem,w = resources
                    self.used_cpu -= cpu
                    self.used_memory -= mem
                    self.slots[w] = None
                with database.transaction() as con:
                    con.execute("UPDATE jobs SET status=?,error=?,finished_at=? WHERE id=?",
                                (status,error,time.time(),jid))

    def recover_orphaned_jobs(self):
        with database.transaction() as con:
            cur = con.execute("""UPDATE jobs SET status='queued',worker_id=NULL,started_at=NULL,
            error='Requeued after scheduler restart' WHERE status='running'""")
        return cur.rowcount

    def cluster_status(self):
        counts = {s:0 for s in ("queued","running","completed","failed","cancelled")}
        with database.connect() as con:
            rows = con.execute("SELECT status,COUNT(*) n FROM jobs GROUP BY status").fetchall()
        for row in rows:
            counts[row["status"]] = row["n"]
        return {"workers":self.worker_count,"cpu_capacity":self.cpu_capacity,
                "memory_capacity_mb":self.memory_capacity_mb,**counts}
