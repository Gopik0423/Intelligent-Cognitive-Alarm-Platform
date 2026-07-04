from pydantic import BaseModel
from typing import Optional


class AlarmCreate(BaseModel):
    user_id: int
    title: str
    alarm_time: str
    days: Optional[str] = None
    ringtone: Optional[str] = "Default"
    vibration: Optional[bool] = True


class AlarmUpdate(BaseModel):
    title: Optional[str] = None
    alarm_time: Optional[str] = None
    days: Optional[str] = None
    ringtone: Optional[str] = None
    vibration: Optional[bool] = None
    is_active: Optional[bool] = None


class AlarmResponse(BaseModel):
    id: int
    user_id: int
    title: str
    alarm_time: str
    days: Optional[str]
    ringtone: str
    vibration: bool
    is_active: bool

    class Config:
        from_attributes = True