from fastapi import FastAPI

from routes import user

from database.db import engine
from models.user import User

User.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)


@app.get("/")
def home():
    return {
        "message": "Backend is successfully running"
    }