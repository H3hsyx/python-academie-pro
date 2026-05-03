from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models import Course, Lesson, Module, Quiz, User
from app.schemas import CoursePublic, LessonDetail, LessonListItem, ModulePublic, QuizPublic
from app.services.progress import add_xp, award_eligible_badges, mark_progress

router = APIRouter(tags=["courses"])


@router.get("/courses", response_model=list[CoursePublic])
def list_courses(
    level: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
) -> list[Course]:
    stmt = select(Course).order_by(Course.order_index)
    if level:
        stmt = stmt.where(Course.level == level)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(or_(Course.title.ilike(pattern), Course.description.ilike(pattern)))
    return list(db.scalars(stmt).all())


@router.get("/courses/{course_id}", response_model=CoursePublic)
def get_course(course_id: int, db: Session = Depends(get_db)) -> Course:
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Parcours introuvable")
    return course


@router.get("/courses/{course_id}/modules", response_model=list[ModulePublic])
def list_modules(course_id: int, db: Session = Depends(get_db)) -> list[Module]:
    return list(db.scalars(select(Module).where(Module.course_id == course_id).order_by(Module.order_index)).all())


@router.get("/modules/{module_id}/lessons", response_model=list[LessonListItem])
def list_lessons(module_id: int, db: Session = Depends(get_db)) -> list[Lesson]:
    return list(db.scalars(select(Lesson).where(Lesson.module_id == module_id).order_by(Lesson.order_index)).all())


@router.get("/lessons/{lesson_id}", response_model=LessonDetail)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)) -> Lesson:
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lecon introuvable")
    return lesson


@router.post("/lessons/{lesson_id}/complete")
def complete_lesson(
    lesson_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lecon introuvable")
    progress = mark_progress(db, current_user, "lesson", lesson_id, 100)
    add_xp(current_user, 15)
    award_eligible_badges(db, current_user)
    db.commit()
    return {"message": "Lecon terminee", "progress_id": progress.id, "xp": current_user.xp, "level": current_user.level}


@router.get("/modules/{module_id}/quizzes", response_model=list[QuizPublic])
def module_quizzes(module_id: int, db: Session = Depends(get_db)):
    quizzes = db.scalars(select(Quiz).where(Quiz.module_id == module_id)).all()
    return [
        QuizPublic(
            id=q.id,
            module_id=q.module_id,
            lesson_id=q.lesson_id,
            title=q.title,
            description=q.description,
            difficulty=q.difficulty,
            time_limit_minutes=q.time_limit_minutes,
            questions=[
                {"id": item.id, "question": item.question, "question_type": item.question_type, "options": item.options, "points": item.points}
                for item in q.questions
            ],
        )
        for q in quizzes
    ]
