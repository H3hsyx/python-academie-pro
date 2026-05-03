from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models import Favorite, User, UserBadge, UserProgress
from app.schemas import FavoriteCreate, FavoritePublic, UserBadgePublic, UserProgressPublic, UserPublic

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=UserPublic)
def profile(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.get("/badges", response_model=list[UserBadgePublic])
def my_badges(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return list(db.scalars(select(UserBadge).where(UserBadge.user_id == current_user.id)).all())


@router.get("/progress", response_model=list[UserProgressPublic])
def my_progress(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return list(db.scalars(select(UserProgress).where(UserProgress.user_id == current_user.id)).all())


@router.get("/favorites", response_model=list[FavoritePublic])
def my_favorites(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return list(db.scalars(select(Favorite).where(Favorite.user_id == current_user.id)).all())


@router.post("/favorites", response_model=FavoritePublic)
def add_favorite(payload: FavoriteCreate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    favorite = db.scalar(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.entity_type == payload.entity_type,
            Favorite.entity_id == payload.entity_id,
        )
    )
    if favorite:
        return favorite
    favorite = Favorite(user_id=current_user.id, entity_type=payload.entity_type, entity_id=payload.entity_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite
