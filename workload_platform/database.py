import sqlite3
from pathlib import Path
from contextlib import contextmanager
from .config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
 id TEXT PRIMARY KEY, name TEXT NOT NULL, command TEXT NOT NULL,
 cpu INTEGER NOT NULL, memory_mb INTEGER NOT NULL, priority INTEGER NOT NULL,
 duration_s REAL NOT NULL, fail_probability REAL NOT NULL DEFAULT 0,
 status TEXT NOT NULL, worker_id TEXT, submitted_at REAL NOT NULL,
 started_at REAL, finished_at REAL, error TEXT
);
CREATE INDEX IF NOT EXISTS idx_jobs_queue ON jobs(status, priority DESC, submitted_at ASC);
"""

def connect():
    Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(settings.db_path, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    return con

def init_db():
    with connect() as con:
        con.executescript(SCHEMA)

@contextmanager
def transaction():
    con = connect()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
