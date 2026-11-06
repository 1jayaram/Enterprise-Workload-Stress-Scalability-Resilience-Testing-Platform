from workload_platform import database
from workload_platform.scheduler import Scheduler

def test_running_job_is_requeued_after_restart(tmp_path):
    import workload_platform.config as cfg
    cfg.settings=type(cfg.settings)(db_path=str(tmp_path/"recovery.db"),workers=1,cpu_capacity=2,memory_mb=512)
    database.settings=cfg.settings
    database.init_db()
    with database.transaction() as con:
        con.execute("""INSERT INTO jobs
        (id,name,command,cpu,memory_mb,priority,duration_s,fail_probability,status,submitted_at,started_at)
        VALUES ('orphan','orphan','x',1,10,1,1,0,'running',1,2)""")
    s=Scheduler(workers=1,cpu_capacity=2,memory_capacity_mb=512)
    assert s.recover_orphaned_jobs()==1
    assert s.get_job("orphan")["status"]=="queued"
