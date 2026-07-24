from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.database.dependencies import get_db
from Backend.models.wake_goal import WakeGoal
from Backend.models.user import User
from Backend.schemas.wake_goal import WakeGoalCreate, WakeGoalUpdate
from Backend.auth import verify_token

router = APIRouter(prefix="/wake-goal", tags=["Wake Goal"])


@router.post("/")
def create_wake_goal(
    wake_goal: WakeGoalCreate,
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_goal = db.query(WakeGoal).filter(
        WakeGoal.user_id == user.id
    ).first()

    if existing_goal:
        raise HTTPException(
            status_code=400,
            detail="Wake Goal already exists"
        )

    new_goal = WakeGoal(
        user_id=user.id,
        goal_time=wake_goal.goal_time,
        description=wake_goal.description,
        is_enabled=wake_goal.is_enabled
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return {
        "message": "Wake Goal Created Successfully",
        "data": new_goal
    }


@router.get("/")
def get_wake_goal(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    goal = db.query(WakeGoal).filter(
        WakeGoal.user_id == user.id
    ).first()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Wake Goal not found"
        )

    return goal


@router.put("/")
def update_wake_goal(
    wake_goal: WakeGoalUpdate,
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    db_goal = db.query(WakeGoal).filter(
        WakeGoal.user_id == user.id
    ).first()

    if db_goal is None:
        raise HTTPException(
            status_code=404,
            detail="Wake Goal not found"
        )

    db_goal.goal_time = wake_goal.goal_time
    db_goal.description = wake_goal.description
    db_goal.is_enabled = wake_goal.is_enabled

    db.commit()
    db.refresh(db_goal)

    return {
        "message": "Wake Goal Updated Successfully",
        "data": db_goal
    }


@router.delete("/")
def delete_wake_goal(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    db_goal = db.query(WakeGoal).filter(
        WakeGoal.user_id == user.id
    ).first()

    if db_goal is None:
        raise HTTPException(
            status_code=404,
            detail="Wake Goal not found"
        )

    db.delete(db_goal)
    db.commit()

    return {
        "message": "Wake Goal Deleted Successfully"
    }