from typing import Literal, Optional
from pydantic import BaseModel, Field


class DifficultyResponse(BaseModel):
    user_id: int
    difficulty_level: int
    correct_streak: int
    fail_streak: int

    class Config:
        from_attributes = True


class DifficultyUpdateRequest(BaseModel):
    user_id: int
    action: Literal["correct", "fail", "set"]
    level: Optional[int] = Field(default=None, ge=1, le=4)
