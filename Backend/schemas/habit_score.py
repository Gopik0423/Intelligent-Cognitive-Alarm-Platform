from pydantic import BaseModel, Field


class HabitMetrics(BaseModel):
    wake_up_consistency: float = Field(ge=0, le=100, default=0)
    challenge_completion: float = Field(ge=0, le=100, default=0)
    snooze_reduction: float = Field(ge=0, le=100, default=0)
    sleep_schedule_adherence: float = Field(ge=0, le=100, default=0)


class HabitScoreUpdateRequest(HabitMetrics):
    user_id: int


class HabitScoreResponse(BaseModel):
    user_id: int
    habit_score: float
    wake_up_consistency: float
    challenge_completion: float
    snooze_reduction: float
    sleep_schedule_adherence: float

    class Config:
        from_attributes = True
