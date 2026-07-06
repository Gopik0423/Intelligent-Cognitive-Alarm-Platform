from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.habit import Habit
from models.user import User
from schemas.habit import HabitCreate, HabitUpdate
from auth import verify_token

router = APIRouter(prefix="/habit", tags=["Habit"])


@router.post("/")
def create_habit(
    habit: HabitCreate,
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_habit = db.query(Habit).filter(
        Habit.user_id == user.id
    ).first()

    if existing_habit:
        raise HTTPException(
            status_code=400,
            detail="Habit already exists"
        )

    new_habit = Habit(
        user_id=user.id,
        habit_name=habit.habit_name,
        productivity_type=habit.productivity_type
    )

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return {
        "message": "Habit Created Successfully",
        "data": new_habit
    }


@router.get("/")
def get_habit(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    habit = db.query(Habit).filter(
        Habit.user_id == user.id
    ).first()

    if habit is None:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    return habit


@router.put("/")
def update_habit(
    habit: HabitUpdate,
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    db_habit = db.query(Habit).filter(
        Habit.user_id == user.id
    ).first()

    if db_habit is None:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    db_habit.habit_name = habit.habit_name
    db_habit.productivity_type = habit.productivity_type

    db.commit()
    db.refresh(db_habit)

    return {
        "message": "Habit Updated Successfully",
        "data": db_habit
    }


@router.delete("/")
def delete_habit(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    db_habit = db.query(Habit).filter(
        Habit.user_id == user.id
    ).first()

    if db_habit is None:
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    db.delete(db_habit)
    db.commit()

    return {
        "message": "Habit Deleted Successfully"
    }