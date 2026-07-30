from datetime import time, date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

ALARM_TYPES = {"daily", "weekly", "one_time", "smart"}


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
    challenge_time_limit_seconds: int = 60

    @model_validator(mode="after")
    def validate_schedule(self):
        if self.alarm_type not in ALARM_TYPES:
            raise ValueError("alarm_type must be daily, weekly, one_time, or smart")
        if self.alarm_type == "one_time" and not self.one_time_date:
            raise ValueError("one_time_date is required for one_time alarms")
        if self.alarm_type == "weekly" and not self.repeat_days:
            raise ValueError("repeat_days is required for weekly alarms")
        if self.repeat_days and any(day not in range(7) for day in self.repeat_days):
            raise ValueError("repeat_days must use Monday=0 through Sunday=6")
        if not 1 <= self.snooze_duration_minutes <= 60:
            raise ValueError("snooze_duration_minutes must be between 1 and 60")
        if not 0 <= self.max_snooze_count <= 10:
            raise ValueError("max_snooze_count must be between 0 and 10")
        if not 10 <= self.challenge_time_limit_seconds <= 600:
            raise ValueError("challenge_time_limit_seconds must be between 10 and 600")
        return self


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
    challenge_time_limit_seconds: Optional[int] = Field(default=None, ge=10, le=600)

    @field_validator("alarm_type")
    @classmethod
    def validate_alarm_type(cls, value):
        if value is not None and value not in ALARM_TYPES:
            raise ValueError("alarm_type must be daily, weekly, one_time, or smart")
        return value

    @field_validator("repeat_days")
    @classmethod
    def validate_repeat_days(cls, value):
        if value and any(day not in range(7) for day in value):
            raise ValueError("repeat_days must use Monday=0 through Sunday=6")
        return value


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
    challenge_time_limit_seconds: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator("repeat_days", mode="before")
    @classmethod
    def parse_repeat_days(cls, value):
        if isinstance(value, str):
            return [int(day) for day in value.split(",") if day]
        return value


class DeviceTokenCreate(BaseModel):
    token: str = Field(min_length=10, max_length=4096)
    platform: str = Field(default="unknown", max_length=30)


class SnoozeRequest(BaseModel):
    event_id: Optional[int] = None
