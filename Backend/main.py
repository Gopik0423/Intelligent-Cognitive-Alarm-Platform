from fastapi import FastAPI
from sqlalchemy import inspect, text

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
    verification,
    analytics,
    recommendation,
    difficulty,
    habit_score,
)
from models.user import User
from models.alarm import Alarm
from models.profile import Profile
from models.sleep import Sleep
from models.wake_goal import WakeGoal
from models.habit import Habit
from models.challenge import Challenge
from models.performance import Performance
from models.verification import WakeupVerification
from models.analytics import Analytics
from models.difficulty import DifficultyLevel
from models.habit_score import HabitScore

User.metadata.create_all(bind=engine)
Alarm.metadata.create_all(bind=engine)
Profile.metadata.create_all(bind=engine)
Sleep.metadata.create_all(bind=engine)
WakeGoal.metadata.create_all(bind=engine)
Habit.metadata.create_all(bind=engine)
Challenge.metadata.create_all(bind=engine)
Performance.metadata.create_all(bind=engine)
WakeupVerification.metadata.create_all(bind=engine)
Analytics.metadata.create_all(bind=engine)
DifficultyLevel.metadata.create_all(bind=engine)
HabitScore.metadata.create_all(bind=engine)

if "users" in inspect(engine).get_table_names():
    user_columns = {
        column["name"] for column in inspect(engine).get_columns("users")
    }
    if "date_of_birth" not in user_columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE users ADD COLUMN date_of_birth DATE")
            )

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
app.include_router(analytics.router)
app.include_router(recommendation.router)
app.include_router(difficulty.router)
app.include_router(habit_score.router)

@app.get("/")
def home():
    return {"message": "Backend is successfully running"}
