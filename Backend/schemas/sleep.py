from pydantic import BaseModel


class SleepCreate(BaseModel):
    sleep_time: str
    wake_time: str


class SleepUpdate(BaseModel):
    sleep_time: str
    wake_time: str


class SleepResponse(BaseModel):
    id: int
    user_id: int
    sleep_time: str
    wake_time: str

    class Config:
        from_attributes = True