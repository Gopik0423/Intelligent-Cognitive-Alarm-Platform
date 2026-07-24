from pydantic import BaseModel, Field

class ProfileCreate(BaseModel):
    full_name: str
    age: int = Field(..., ge=4, le=120)
    gender: str
    timezone: str


class ProfileUpdate(BaseModel):
    full_name: str
    age:int = Field(..., ge=4, le=120)
    gender: str
    timezone: str


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    age: int
    gender: str
    timezone: str

    class Config:
        from_attributes = True
