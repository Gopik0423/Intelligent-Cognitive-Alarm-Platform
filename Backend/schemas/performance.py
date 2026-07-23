from pydantic import BaseModel
from datetime import datetime


class PerformanceCreate(BaseModel):
    user_id: int
    challenge_type: str

    attempts: int
    accuracy: float
    score: int
    success: bool
    completion_time: float

    # Week 3 Metrics
    wakeup_consistency: float
    challenge_completion: float
    snooze_count: int
    sleep_schedule_adherence: float


class PerformanceOut(PerformanceCreate):
    id: int
    completed_at: datetime

    class Config:
        orm_mode = True