from datetime import date

from pydantic import BaseModel, model_validator


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str
    date_of_birth: date
    gender: str = "Not specified"
    timezone: str = "Asia/Kolkata"

    @model_validator(mode="after")
    def validate_minimum_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        if age < 4:
            raise ValueError("User must be at least 4 years old")
        return self

class UserLogin(BaseModel):
    email: str
    password: str
