from datetime import time, date, datetime
from typing import List, Optional
from pydantic import BaseModel


class AlarmCreate(BaseModel):
    label: str = "Alarm"
    alarm_time: time
    alarm_type: str = "daily"
    repeat_days: Optional[List[int]] = None
    one_time_date: Optional[date] = None
    snooze_enabled: bool = True
    snooze_duration_minutes: int = 5
    max_snooze_count: int = 3
    challenge_type: str = "math"
    difficulty: str = "easy"


class AlarmUpdate(BaseModel):
    label: Optional[str] = None
    alarm_time: Optional[time] = None
    alarm_type: Optional[str] = None
    repeat_days: Optional[List[int]] = None
    one_time_date: Optional[date] = None
    is_active: Optional[bool] = None
    snooze_enabled: Optional[bool] = None
    snooze_duration_minutes: Optional[int] = None
    max_snooze_count: Optional[int] = None
    challenge_type: Optional[str] = None
    difficulty: Optional[str] = None


class AlarmOut(BaseModel):
    id: int
    user_id: int
    label: str
    alarm_time: time
    alarm_type: str
    repeat_days: Optional[List[int]] = None
    one_time_date: Optional[date] = None
    is_active: bool
    snooze_enabled: bool
    snooze_duration_minutes: int
    max_snooze_count: int
    challenge_type: str
    difficulty: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
