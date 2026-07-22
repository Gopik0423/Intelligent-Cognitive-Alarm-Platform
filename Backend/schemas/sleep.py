from datetime import time
from pydantic import BaseModel


class SleepCreate(BaseModel):
    sleep_time: time
    wake_time: time


class SleepUpdate(BaseModel):
    sleep_time: time
    wake_time: time


class SleepResponse(BaseModel):
    id: int
    user_id: int
    sleep_time: time
    wake_time: time

    class Config:
        from_attributes = True