from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class PerformanceCreate(BaseModel):
    user_id: int
    challenge_type: str

    attempts: int
    accuracy: float
    score: int
    success: bool
    completion_time: float

    wakeup_consistency: Optional[float] = None
    challenge_completion: Optional[float] = None
    snooze_count: Optional[int] = None
    sleep_schedule_adherence: Optional[float] = None


class PerformanceOut(PerformanceCreate):
    id: int
    difficulty: Optional[str] = None
    completed_at: datetime

    model_config = ConfigDict(from_attributes=True)