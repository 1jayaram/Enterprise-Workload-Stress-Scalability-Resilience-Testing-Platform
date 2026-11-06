import os,tempfile,pytest
import workload_platform.config as cfg
import workload_platform.database as db
from workload_platform.api import app,scheduler
from fastapi.testclient import TestClient

@pytest.fixture(scope="session",autouse=True)
def isolated_db():
    original=cfg.settings
    path=tempfile.mktemp(suffix=".sqlite3")
    cfg.settings=type(original)(db_path=path,workers=2,cpu_capacity=4,memory_mb=1024)
    db.settings=cfg.settings
    scheduler.worker_count=2; scheduler.cpu_capacity=4; scheduler.memory_capacity_mb=1024
    yield
    try: os.remove(path)
    except OSError: pass

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c: yield c
