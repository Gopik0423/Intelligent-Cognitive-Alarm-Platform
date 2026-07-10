from fastapi import FastAPI
from Backend.database.db import engine

from Backend.routes import user, alarm, profile, sleep, wake_goal, habit, challenge, performance, verification

from Backend.models.user import User
from Backend.models.alarm import Alarm
from Backend.models.profile import Profile
from Backend.models.sleep import Sleep
from Backend.models.wake_goal import WakeGoal
from Backend.models.habit import Habit
from Backend.models.challenge import Challenge
from Backend.models.performance import Performance
from Backend.models.verification import WakeupVerification

User.metadata.create_all(bind=engine)
Alarm.metadata.create_all(bind=engine)
Profile.metadata.create_all(bind=engine)
Sleep.metadata.create_all(bind=engine)
WakeGoal.metadata.create_all(bind=engine)
Habit.metadata.create_all(bind=engine)
Challenge.metadata.create_all(bind=engine)
Performance.metadata.create_all(bind=engine)
WakeupVerification.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(alarm.router)
app.include_router(profile.router)
app.include_router(sleep.router)
app.include_router(wake_goal.router)
app.include_router(habit.router)
app.include_router(challenge.router)
app.include_router(performance.router)
app.include_router(verification.router)

@app.get("/")
def home():
    return {"message": "Backend is successfully running"}
