from pydantic import BaseModel


class AnalyticsCreate(BaseModel):
    user_id: int
    challenge_type: str
    completion_time: int
    snooze_count: int
    success: bool


class AnalyticsResponse(AnalyticsCreate):
    id: int

    class Config:
        from_attributes = True