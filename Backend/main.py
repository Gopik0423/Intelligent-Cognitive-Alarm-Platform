from fastapi import FastAPI

from routes import user
from routes import alarm

from database.db import engine
from models.user import User
from models.alarm import Alarm
from routes import alarm
from models.alarm import Alarm

Alarm.metadata.create_all(bind=engine)

app.include_router(alarm.router)

User.metadata.create_all(bind=engine)
Alarm.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(alarm.router)


@app.get("/")
def home():
    return {
        "message": "Backend is successfully running"
    }
    