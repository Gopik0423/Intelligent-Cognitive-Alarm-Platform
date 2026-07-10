from pydantic import BaseModel
from datetime import datetime


class PerformanceCreate(BaseModel):
    user_id: int
    challenge_type: str
    attempts: int
    accuracy: float
    success: bool
    completion_time: float


class PerformanceOut(PerformanceCreate):
    id: int
    completed_at: datetime

    class Config:
        orm_mode = True
