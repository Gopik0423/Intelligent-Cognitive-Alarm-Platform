from fastapi import FastAPI
from database.db import engine

<<<<<<< HEAD
from routes import user
from routes import profile
from routes import sleep
from routes import wake_goal
from routes import habit
=======
from routes import user, alarm
>>>>>>> origin/feature/alarm-management-v2

from models.user import User
<<<<<<< HEAD
from models.profile import Profile   
from models.sleep import Sleep
from models.wake_goal import WakeGoal
from models.habit import Habit

User.metadata.create_all(bind=engine)
Profile.metadata.create_all(bind=engine)   
Sleep.metadata.create_all(bind=engine)
WakeGoal.metadata.create_all(bind=engine)
Habit.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user.router)
app.include_router(profile.router)
app.include_router(sleep.router)
app.include_router(wake_goal.router)
app.include_router(habit.router)
=======
from models.alarm import Alarm

User.metadata.create_all(bind=engine)
Alarm.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(alarm.router)

>>>>>>> origin/feature/alarm-management-v2

@app.get("/")
def home():
    return {
        "message": "Backend is successfully running"
<<<<<<< HEAD
    }

print("test change")
=======
    }
>>>>>>> origin/feature/alarm-management-v2
