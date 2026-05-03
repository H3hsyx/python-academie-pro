from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Challenge, ResourceItem
from app.schemas import ChallengePublic, ResourceItemPublic

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=list[ResourceItemPublic])
def list_resources(kind: str | None = None, level: str | None = None, q: str | None = None, db: Session = Depends(get_db)):
    stmt = select(ResourceItem).order_by(ResourceItem.kind, ResourceItem.title)
    if kind:
        stmt = stmt.where(ResourceItem.kind == kind)
    if level:
        stmt = stmt.where(ResourceItem.level == level)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(or_(ResourceItem.title.ilike(pattern), ResourceItem.content.ilike(pattern)))
    return list(db.scalars(stmt).all())


@router.get("/{resource_id}", response_model=ResourceItemPublic)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    item = db.get(ResourceItem, resource_id)
    if not item:
        raise HTTPException(status_code=404, detail="Ressource introuvable")
    return item


@router.get("/challenges/list", response_model=list[ChallengePublic])
def list_challenges(level: str | None = None, theme: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Challenge).order_by(Challenge.id)
    if level:
        stmt = stmt.where(Challenge.level == level)
    if theme:
        stmt = stmt.where(Challenge.theme == theme)
    return list(db.scalars(stmt).all())
