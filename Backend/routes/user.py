from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database.db import SessionLocal
from models.user import User
from schemas.user import UserCreate, UserLogin
from auth import create_access_token, verify_token, require_role

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return {"message": "Email already registered"}

    new_user = User(
        name=user.name,
        email=user.email,
        password=pwd_context.hash(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": new_user
    }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return {"message": "User not found"}

    if not pwd_context.verify(user.password, db_user.password):
        return {"message": "Invalid password"}

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/profile")
def profile(payload=Depends(verify_token)):
    return {
        "message": "Profile Access Successful",
        "user": payload
    }


@router.get("/user")
def user_dashboard(payload=Depends(require_role("User"))):
    return {
        "message": "Welcome User",
        "user": payload
    }


@router.get("/admin")
def admin_dashboard(payload=Depends(require_role("Admin"))):
    return {
        "message": "Welcome Admin",
        "user": payload
    }


@router.get("/coach")
def coach_dashboard(payload=Depends(require_role("Wellness Coach"))):
    return {
        "message": "Welcome Wellness Coach",
        "user": payload
    }