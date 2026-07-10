from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models import ChallengeDifficulty, ChallengeType
from app.schemas import ChallengeCreate, ChallengeRead, ChallengeUpdate

router = APIRouter(prefix="/challenges", tags=["challenges"])


@router.get("", response_model=list[ChallengeRead])
def read_challenges(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    challenge_type: ChallengeType | None = Query(default=None, alias="type"),
    difficulty: ChallengeDifficulty | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[ChallengeRead]:
    """Return all challenges with optional filters."""

    return crud.get_challenges(
        db=db,
        skip=skip,
        limit=limit,
        challenge_type=challenge_type.value if challenge_type is not None else None,
        difficulty=difficulty.value if difficulty is not None else None,
    )


@router.get("/{challenge_id}", response_model=ChallengeRead)
def read_challenge(
    challenge_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
) -> ChallengeRead:
    """Return one challenge by id."""

    challenge = crud.get_challenge(db, challenge_id)
    if challenge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
    return challenge


@router.get("/random", response_model=ChallengeRead)
def read_random_challenge(db: Session = Depends(get_db)) -> ChallengeRead:
    """Return a random challenge."""

    challenge = crud.get_random_challenge(db)
    if challenge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No challenges available")
    return challenge


@router.get("/type/{challenge_type}", response_model=list[ChallengeRead])
def read_challenges_by_type(
    challenge_type: ChallengeType,
    db: Session = Depends(get_db),
) -> list[ChallengeRead]:
    """Return challenges matching a given type."""

    return crud.get_challenges(db, challenge_type=challenge_type.value)


@router.get("/difficulty/{difficulty}", response_model=list[ChallengeRead])
def read_challenges_by_difficulty(
    difficulty: ChallengeDifficulty,
    db: Session = Depends(get_db),
) -> list[ChallengeRead]:
    """Return challenges matching a given difficulty."""

    return crud.get_challenges(db, difficulty=difficulty.value)


@router.post("", response_model=ChallengeRead, status_code=status.HTTP_201_CREATED)
def create_challenge(
    challenge_in: ChallengeCreate,
    db: Session = Depends(get_db),
) -> ChallengeRead:
    """Create a new challenge."""

    return crud.create_challenge(db, challenge_in)


@router.put("/{challenge_id}", response_model=ChallengeRead)
def update_challenge(
    challenge_id: int = Path(..., ge=1),
    challenge_in: ChallengeUpdate = ...,  # type: ignore[assignment]
    db: Session = Depends(get_db),
) -> ChallengeRead:
    """Update an existing challenge."""

    existing = crud.get_challenge(db, challenge_id)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
    return crud.update_challenge(db, existing, challenge_in)


@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_challenge(
    challenge_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
) -> None:
    """Delete a challenge."""

    existing = crud.get_challenge(db, challenge_id)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
    crud.delete_challenge(db, existing)
