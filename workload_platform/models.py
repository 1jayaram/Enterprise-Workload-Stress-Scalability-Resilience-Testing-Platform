from pydantic import BaseModel, Field
from typing import Literal, Optional

class JobCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    command: str = Field(default="simulated-task", max_length=500)
    cpu: int = Field(default=1, ge=1, le=64)
    memory_mb: int = Field(default=128, ge=1, le=1048576)
    priority: int = Field(default=0, ge=0, le=100)
    duration_s: float = Field(default=1.0, gt=0, le=3600)
    fail_probability: float = Field(default=0.0, ge=0, le=1)

class JobOut(BaseModel):
    id: str
    name: str
    command: str
    cpu: int
    memory_mb: int
    priority: int
    duration_s: float
    status: Literal["queued","running","completed","failed","cancelled"]
    worker_id: Optional[str] = None
    submitted_at: float
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    error: Optional[str] = None
