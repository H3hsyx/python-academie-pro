from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import require_admin
from app.models import Comment, Course, Exercise, Lesson, Project, QuizResult, User
from app.schemas import CoursePublic, ExercisePublic, LessonDetail, ProjectDetail, UserPublic
from app.services.text import slugify

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def stats(_: Annotated[User, Depends(require_admin)], db: Session = Depends(get_db)):
    return {
        "users": db.scalar(select(func.count(User.id))) or 0,
        "courses": db.scalar(select(func.count(Course.id))) or 0,
        "lessons": db.scalar(select(func.count(Lesson.id))) or 0,
        "exercises": db.scalar(select(func.count(Exercise.id))) or 0,
        "projects": db.scalar(select(func.count(Project.id))) or 0,
        "quiz_results": db.scalar(select(func.count(QuizResult.id))) or 0,
        "comments": db.scalar(select(func.count(Comment.id))) or 0,
    }


@router.get("/users", response_model=list[UserPublic])
def users(_: Annotated[User, Depends(require_admin)], db: Session = Depends(get_db)):
    return list(db.scalars(select(User).order_by(User.created_at.desc()).limit(200)).all())


@router.post("/courses", response_model=CoursePublic)
def create_course(payload: dict[str, Any], _: Annotated[User, Depends(require_admin)], db: Session = Depends(get_db)):
    title = payload.get("title") or "Nouveau parcours"
    item = Course(
        slug=payload.get("slug") or slugify(title),
        title=title,
        description=payload.get("description") or "Description a completer.",
        level=payload.get("level") or "Debutant",
        track_type=payload.get("track_type") or "custom",
        estimated_duration=payload.get("estimated_duration") or "4 semaines",
        objectives=payload.get("objectives") or [],
        final_projects=payload.get("final_projects") or [],
        order_index=payload.get("order_index") or 999,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/lessons/{lesson_id}", response_model=LessonDetail)
def update_lesson(lesson_id: int, payload: dict[str, Any], _: Annotated[User, Depends(require_admin)], db: Session = Depends(get_db)):
    item = db.get(Lesson, lesson_id)
    if not item:
        raise HTTPException(status_code=404, detail="Lecon introuvable")
    for key in ["title", "content", "summary", "difficulty", "objectives", "common_errors", "tips", "mini_exercise", "code_examples"]:
        if key in payload:
            setattr(item, key, payload[key])
    db.commit()
    db.refresh(item)
    return item


@router.post("/exercises", response_model=ExercisePublic)
def create_exercise(payload: dict[str, Any], _: Annotated[User, Depends(require_admin)], db: Session = Depends(get_db)):
    title = payload.get("title") or "Nouvel exercice"
    item = Exercise(
        lesson_id=payload.get("lesson_id"),
        slug=payload.get("slug") or slugify(title),
        title=title,
        description=payload.get("description") or "Enonce a completer.",
        starter_code=payload.get("starter_code") or "",
        expected_output=payload.get("expected_output") or "",
        solution=payload.get("solution") or "",
        optimized_solution=payload.get("optimized_solution") or "",
        explanation=payload.get("explanation") or "",
        difficulty=payload.get("difficulty") or "facile",
        level=payload.get("level") or "Debutant",
        theme=payload.get("theme") or "Python",
        duration_minutes=payload.get("duration_minutes") or 10,
        exercise_type=payload.get("exercise_type") or "ecrire une fonction",
        hints=payload.get("hints") or [],
        tests=payload.get("tests") or [],
        points=payload.get("points") or 10,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.post("/projects", response_model=ProjectDetail)
def create_project(payload: dict[str, Any], _: Annotated[User, Depends(require_admin)], db: Session = Depends(get_db)):
    title = payload.get("title") or "Nouveau projet"
    item = Project(
        slug=payload.get("slug") or slugify(title),
        title=title,
        description=payload.get("description") or "Projet a completer.",
        level=payload.get("level") or "Debutant",
        category=payload.get("category") or "Portfolio",
        estimated_duration=payload.get("estimated_duration") or "4 h",
        objective=payload.get("objective") or "Construire un projet Python utile.",
        skills=payload.get("skills") or [],
        specifications=payload.get("specifications") or "Cahier des charges a completer.",
        steps=payload.get("steps") or [],
        starter_code=payload.get("starter_code") or "",
        hints=payload.get("hints") or [],
        final_code=payload.get("final_code") or "",
        improvements=payload.get("improvements") or [],
        bonus=payload.get("bonus") or "",
        difficulty=payload.get("difficulty") or "moyen",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/comments/{comment_id}")
def hide_comment(comment_id: int, _: Annotated[User, Depends(require_admin)], db: Session = Depends(get_db)):
    item = db.get(Comment, comment_id)
    if not item:
        raise HTTPException(status_code=404, detail="Commentaire introuvable")
    item.is_hidden = True
    db.commit()
    return {"message": "Commentaire masque"}
