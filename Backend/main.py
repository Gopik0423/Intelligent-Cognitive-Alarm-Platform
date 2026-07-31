import asyncio
from contextlib import asynccontextmanager, suppress

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
    reports,
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
from models.alarm_event import AlarmEvent
from models.device_token import DeviceToken
from models.notification_log import NotificationLog
from database.db import SessionLocal
from services.alarm_runtime import process_due_alarms

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
AlarmEvent.metadata.create_all(bind=engine)
DeviceToken.metadata.create_all(bind=engine)
NotificationLog.metadata.create_all(bind=engine)

if "users" in inspect(engine).get_table_names():
    user_columns = {
        column["name"] for column in inspect(engine).get_columns("users")
    }
    if "date_of_birth" not in user_columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE users ADD COLUMN date_of_birth DATE")
            )

if "alarms" in inspect(engine).get_table_names():
    alarm_columns = {column["name"] for column in inspect(engine).get_columns("alarms")}
    if "challenge_time_limit_seconds" not in alarm_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE alarms ADD COLUMN challenge_time_limit_seconds INTEGER NOT NULL DEFAULT 60"))

async def alarm_scheduler():
    """Poll once a minute; each database event makes processing idempotent."""
    while True:
        db = SessionLocal()
        try:
            process_due_alarms(db)
        finally:
            db.close()
        await asyncio.sleep(30)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(alarm_scheduler())
    yield
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


app = FastAPI(title="Intelligent Cognitive Alarm Platform", lifespan=lifespan)
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
app.include_router(reports.router)

@app.get("/")
def home():
    return {"message": "Backend is successfully running"}
