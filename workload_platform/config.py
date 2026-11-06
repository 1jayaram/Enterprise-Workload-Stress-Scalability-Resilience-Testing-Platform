import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    db_path: str = os.getenv("APP_DB_PATH", "data/scheduler.db")
    workers: int = int(os.getenv("APP_WORKERS", "4"))
    cpu_capacity: int = int(os.getenv("APP_CPU_CAPACITY", "8"))
    memory_mb: int = int(os.getenv("APP_MEMORY_MB", "8192"))

settings = Settings()
