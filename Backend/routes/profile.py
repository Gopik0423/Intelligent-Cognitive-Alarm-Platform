from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.profile import Profile
from models.user import User
from schemas.profile import ProfileCreate, ProfileUpdate
from auth import verify_token

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/")
def create_profile(
    profile: ProfileCreate,
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_profile = db.query(Profile).filter(Profile.user_id == user.id).first()

    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    new_profile = Profile(
        user_id=user.id,
        full_name=profile.full_name,
        age=profile.age,
        gender=profile.gender,
        timezone=profile.timezone
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {
        "message": "Profile Created Successfully",
        "data": new_profile
    }


@router.get("/")
def get_profile(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(Profile).filter(Profile.user_id == user.id).first()

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("/")
def update_profile(
    profile: ProfileUpdate,
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    db_profile = db.query(Profile).filter(Profile.user_id == user.id).first()

    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    db_profile.full_name = profile.full_name
    db_profile.age = profile.age
    db_profile.gender = profile.gender
    db_profile.timezone = profile.timezone

    db.commit()
    db.refresh(db_profile)

    return {
        "message": "Profile Updated Successfully",
        "data": db_profile
    }


@router.delete("/")
def delete_profile(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):

    email = payload["sub"]

    user = db.query(User).filter(User.email == email).first()

    db_profile = db.query(Profile).filter(Profile.user_id == user.id).first()

    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(db_profile)
    db.commit()

    return {
        "message": "Profile Deleted Successfully"
    }