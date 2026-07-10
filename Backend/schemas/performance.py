from pydantic import BaseModel


class PerformanceCreate(BaseModel):
    user_id: int
    challenge_type: str
    difficulty: str
    completion_time: int
    attempts: int
    score: int
    success: bool