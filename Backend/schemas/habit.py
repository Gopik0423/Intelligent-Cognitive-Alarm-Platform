from pydantic import BaseModel


class HabitCreate(BaseModel):
    habit_name: str
    productivity_type: str


class HabitUpdate(BaseModel):
    habit_name: str
    productivity_type: str


class HabitResponse(BaseModel):
    id: int
    user_id: int
    habit_name: str
    productivity_type: str

    class Config:
        from_attributes = True