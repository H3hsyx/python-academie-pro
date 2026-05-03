from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models import Comment, Discussion, User
from app.schemas import CommentCreate, CommentPublic, DiscussionCreate, DiscussionPublic
from app.services.text import slugify

router = APIRouter(prefix="/community", tags=["community"])


@router.get("/discussions", response_model=list[DiscussionPublic])
def list_discussions(theme: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Discussion).order_by(Discussion.pinned.desc(), Discussion.created_at.desc()).limit(100)
    if theme:
        stmt = stmt.where(Discussion.theme == theme)
    return list(db.scalars(stmt).all())


@router.post("/discussions", response_model=DiscussionPublic)
def create_discussion(payload: DiscussionCreate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    base = slugify(payload.title)
    slug = base
    index = 2
    while db.scalar(select(Discussion).where(Discussion.slug == slug)):
        slug = f"{base}-{index}"
        index += 1
    discussion = Discussion(user_id=current_user.id, title=payload.title, slug=slug, body=payload.body, theme=payload.theme)
    db.add(discussion)
    db.commit()
    db.refresh(discussion)
    return discussion


@router.get("/comments", response_model=list[CommentPublic])
def list_comments(entity_type: str, entity_id: int, db: Session = Depends(get_db)):
    comments = db.scalars(
        select(Comment).where(Comment.entity_type == entity_type, Comment.entity_id == entity_id, Comment.is_hidden.is_(False)).order_by(Comment.created_at)
    ).all()
    return [
        CommentPublic(
            id=item.id,
            entity_type=item.entity_type,
            entity_id=item.entity_id,
            parent_id=item.parent_id,
            content=item.content,
            created_at=item.created_at,
            username=item.user.username if item.user else "utilisateur",
        )
        for item in comments
    ]


@router.post("/comments", response_model=CommentPublic)
def create_comment(payload: CommentCreate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    item = Comment(
        user_id=current_user.id,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        parent_id=payload.parent_id,
        content=payload.content,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return CommentPublic(
        id=item.id,
        entity_type=item.entity_type,
        entity_id=item.entity_id,
        parent_id=item.parent_id,
        content=item.content,
        created_at=item.created_at,
        username=current_user.username,
    )
