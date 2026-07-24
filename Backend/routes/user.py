from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from database.db import SessionLocal
from models.user import User
from schemas.user import UserCreate
from auth import create_access_token, verify_token, require_role

router = APIRouter()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def calculate_age(date_of_birth: date) -> int:
    today = date.today()
    return today.year - date_of_birth.year - (
        (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
    )


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

    # Add this block here
    if user.role == "Admin":
        admin = db.query(User).filter(User.role == "Admin").first()

        if admin:
            return {"message": "Admin already exists"}

    # Existing code
    new_user = User(
        name=user.name,
        email=user.email,
        password=pwd_context.hash(user.password),
        role=user.role,
        date_of_birth=user.date_of_birth,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": new_user,
        "age": calculate_age(new_user.date_of_birth),
    }


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # OAuth2PasswordRequestForm sends 'username' and 'password' fields
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        return {"message": "User not found"}

    if not pwd_context.verify(form_data.password, db_user.password):
        return {"message": "Invalid password"}

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "user_id": db_user.id,
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

@router.get("/admin/users")
def get_all_users(
    payload=Depends(require_role("Admin")),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users

@router.get("/admin/stats")
def admin_stats(
    payload=Depends(require_role("Admin")),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()

    return {
        "total_users": total_users
    }
