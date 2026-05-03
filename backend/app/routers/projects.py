from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models import Project, ProjectSubmission, User
from app.schemas import ProjectDetail, ProjectPublic, ProjectSubmissionCreate, ProjectSubmissionPublic
from app.services.progress import add_xp, award_eligible_badges, mark_progress

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectPublic])
def list_projects(
    level: str | None = None,
    category: str | None = None,
    q: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[Project]:
    stmt = select(Project).order_by(Project.id).limit(min(limit, 200))
    if level:
        stmt = stmt.where(Project.level == level)
    if category:
        stmt = stmt.where(Project.category.ilike(f"%{category}%"))
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(or_(Project.title.ilike(pattern), Project.description.ilike(pattern)))
    return list(db.scalars(stmt).all())


@router.get("/{project_id}", response_model=ProjectDetail)
def get_project(project_id: int, db: Session = Depends(get_db)) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    return project


@router.post("/{project_id}/submit", response_model=ProjectSubmissionPublic)
def submit_project(
    project_id: int,
    payload: ProjectSubmissionCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> ProjectSubmissionPublic:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    submission = ProjectSubmission(
        user_id=current_user.id,
        project_id=project.id,
        repository_url=payload.repository_url,
        notes=payload.notes,
        status="submitted",
    )
    db.add(submission)
    add_xp(current_user, 100)
    mark_progress(db, current_user, "project", project.id, 100)
    award_eligible_badges(db, current_user)
    db.commit()
    db.refresh(submission)
    return ProjectSubmissionPublic(
        id=submission.id,
        project_id=project.id,
        status=submission.status,
        repository_url=submission.repository_url,
        notes=submission.notes,
        created_at=submission.created_at,
        awarded_xp=100,
    )
