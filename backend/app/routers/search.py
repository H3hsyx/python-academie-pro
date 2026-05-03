from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Course, Exercise, Lesson, Project, ResourceItem
from app.schemas import SearchResult

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[SearchResult])
def global_search(q: str = Query(min_length=2), db: Session = Depends(get_db)) -> list[SearchResult]:
    pattern = f"%{q}%"
    results: list[SearchResult] = []

    for item in db.scalars(select(Course).where(or_(Course.title.ilike(pattern), Course.description.ilike(pattern))).limit(8)).all():
        results.append(SearchResult(entity_type="course", entity_id=item.id, title=item.title, description=item.description[:180], url=f"/parcours/{item.id}", level=item.level))
    for item in db.scalars(select(Lesson).where(or_(Lesson.title.ilike(pattern), Lesson.content.ilike(pattern))).limit(8)).all():
        results.append(SearchResult(entity_type="lesson", entity_id=item.id, title=item.title, description=item.summary[:180], url=f"/cours/{item.id}", level=item.difficulty))
    for item in db.scalars(select(Exercise).where(or_(Exercise.title.ilike(pattern), Exercise.description.ilike(pattern))).limit(8)).all():
        results.append(SearchResult(entity_type="exercise", entity_id=item.id, title=item.title, description=item.description[:180], url=f"/exercices/{item.id}", level=item.level))
    for item in db.scalars(select(Project).where(or_(Project.title.ilike(pattern), Project.description.ilike(pattern))).limit(8)).all():
        results.append(SearchResult(entity_type="project", entity_id=item.id, title=item.title, description=item.description[:180], url=f"/projets/{item.id}", level=item.level))
    for item in db.scalars(select(ResourceItem).where(or_(ResourceItem.title.ilike(pattern), ResourceItem.content.ilike(pattern))).limit(8)).all():
        results.append(SearchResult(entity_type="resource", entity_id=item.id, title=item.title, description=item.content[:180], url=f"/ressources/{item.id}", level=item.level))
    return results[:30]
