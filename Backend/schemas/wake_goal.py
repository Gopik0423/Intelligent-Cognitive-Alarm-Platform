from pydantic import BaseModel


class WakeGoalCreate(BaseModel):
    goal_time: str
    description: str
    is_enabled: bool


class WakeGoalUpdate(BaseModel):
    goal_time: str
    description: str
    is_enabled: bool


class WakeGoalResponse(BaseModel):
    id: int
    user_id: int
    goal_time: str
    description: str
    is_enabled: bool

    class Config:
        from_attributes = True
