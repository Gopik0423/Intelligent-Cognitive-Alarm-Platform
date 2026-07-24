from fastapi import FastAPI
from database.db import engine

from routes import (
    user,
    alarm,
    profile,
    sleep,
    wake_goal,
    habit,
    challenge,
    performance,
)

from models.user import User
from models.alarm import Alarm
from models.profile import Profile
from models.sleep import Sleep
from models.wake_goal import WakeGoal
from models.habit import Habit
from models.challenge import Challenge
from models.performance import Performance

User.metadata.create_all(bind=engine)
Alarm.metadata.create_all(bind=engine)
Profile.metadata.create_all(bind=engine)
Sleep.metadata.create_all(bind=engine)
WakeGoal.metadata.create_all(bind=engine)
Habit.metadata.create_all(bind=engine)
Challenge.metadata.create_all(bind=engine)
Performance.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(alarm.router)
app.include_router(profile.router)
app.include_router(sleep.router)
app.include_router(wake_goal.router)
app.include_router(habit.router)
app.include_router(challenge.router)
app.include_router(performance.router)

@app.get("/")
def home():
    return {"message": "Backend is successfully running"}