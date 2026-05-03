from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas import Token, UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    existing = db.scalar(select(User).where(or_(User.email == payload.email, User.username == payload.username)))
    if existing:
        raise HTTPException(status_code=409, detail="Email ou nom utilisateur deja utilise")
    user = User(
        username=payload.username,
        email=str(payload.email),
        password_hash=get_password_hash(payload.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = db.scalar(select(User).where(or_(User.email == form_data.username, User.username == form_data.username)))
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants incorrects")
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    token = create_access_token(str(user.id), {"role": user.role})
    return Token(access_token=token)


@router.get("/me", response_model=UserPublic)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
