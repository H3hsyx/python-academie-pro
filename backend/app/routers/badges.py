from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Badge
from app.schemas import BadgePublic

router = APIRouter(prefix="/badges", tags=["badges"])


@router.get("", response_model=list[BadgePublic])
def list_badges(db: Session = Depends(get_db)):
    return list(db.scalars(select(Badge).order_by(Badge.xp_required, Badge.id)).all())
