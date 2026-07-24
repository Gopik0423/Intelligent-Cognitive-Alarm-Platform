from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.database.dependencies import get_db
from Backend.models.sleep import Sleep
from Backend.models.user import User
from Backend.schemas.sleep import SleepCreate, SleepUpdate
from Backend.auth import verify_token

router = APIRouter(prefix="/sleep", tags=["Sleep Schedule"])


@router.post("/")
def create_sleep_schedule(
    sleep: SleepCreate,
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_schedule = db.query(Sleep).filter(Sleep.user_id == user.id).first()

    if existing_schedule:
        raise HTTPException(
            status_code=400,
            detail="Sleep Schedule already exists"
        )

    new_sleep = Sleep(
        user_id=user.id,
        sleep_time=sleep.sleep_time,
        wake_time=sleep.wake_time
    )

    db.add(new_sleep)
    db.commit()
    db.refresh(new_sleep)

    return {
        "message": "Sleep Schedule Created Successfully",
        "data": new_sleep
    }


@router.get("/")
def get_sleep_schedule(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    sleep = db.query(Sleep).filter(Sleep.user_id == user.id).first()

    if sleep is None:
        raise HTTPException(
            status_code=404,
            detail="Sleep Schedule not found"
        )

    return sleep


@router.put("/")
def update_sleep_schedule(
    sleep: SleepUpdate,
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    db_sleep = db.query(Sleep).filter(Sleep.user_id == user.id).first()

    if db_sleep is None:
        raise HTTPException(
            status_code=404,
            detail="Sleep Schedule not found"
        )

    db_sleep.sleep_time = sleep.sleep_time
    db_sleep.wake_time = sleep.wake_time

    db.commit()
    db.refresh(db_sleep)

    return {
        "message": "Sleep Schedule Updated Successfully",
        "data": db_sleep
    }


@router.delete("/")
def delete_sleep_schedule(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    db_sleep = db.query(Sleep).filter(Sleep.user_id == user.id).first()

    if db_sleep is None:
        raise HTTPException(
            status_code=404,
            detail="Sleep Schedule not found"
        )

    db.delete(db_sleep)
    db.commit()

    return {
        "message": "Sleep Schedule Deleted Successfully"
    }