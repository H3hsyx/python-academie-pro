from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models import ExerciseAttempt, Lesson, ProjectSubmission, QuizResult, User, UserBadge, UserProgress
from app.schemas import DashboardStats, LessonListItem, UserBadgePublic, UserPublic
from app.services.progress import xp_to_next_level

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardStats)
def dashboard(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)) -> DashboardStats:
    total_lessons = db.scalar(select(func.count(Lesson.id))) or 1
    lessons_done = db.scalar(
        select(func.count(UserProgress.id)).where(
            UserProgress.user_id == current_user.id,
            UserProgress.entity_type == "lesson",
            UserProgress.status == "completed",
        )
    ) or 0
    exercises_passed = db.scalar(
        select(func.count(ExerciseAttempt.id)).where(ExerciseAttempt.user_id == current_user.id, ExerciseAttempt.passed.is_(True))
    ) or 0
    projects_done = db.scalar(
        select(func.count(ProjectSubmission.id)).where(ProjectSubmission.user_id == current_user.id)
    ) or 0
    quizzes_passed = db.scalar(
        select(func.count(QuizResult.id)).where(QuizResult.user_id == current_user.id, QuizResult.passed.is_(True))
    ) or 0

    progress_rows = db.scalars(
        select(UserProgress)
        .where(UserProgress.user_id == current_user.id, UserProgress.entity_type == "lesson")
        .order_by(desc(UserProgress.updated_at))
        .limit(1)
    ).all()
    last_lesson = None
    if progress_rows:
        lesson = db.get(Lesson, progress_rows[0].entity_id)
        if lesson:
            last_lesson = LessonListItem.model_validate(lesson)

    completed_lesson_ids = [
        row.entity_id
        for row in db.scalars(
            select(UserProgress).where(
                UserProgress.user_id == current_user.id,
                UserProgress.entity_type == "lesson",
                UserProgress.status == "completed",
            )
        ).all()
    ]
    stmt = select(Lesson).order_by(Lesson.id).limit(5)
    if completed_lesson_ids:
        stmt = stmt.where(Lesson.id.not_in(completed_lesson_ids))
    recommendations = [LessonListItem.model_validate(item) for item in db.scalars(stmt).all()]

    badges = [UserBadgePublic.model_validate(item) for item in db.scalars(select(UserBadge).where(UserBadge.user_id == current_user.id)).all()]
    completion = int((lessons_done / total_lessons) * 100)
    return DashboardStats(
        user=UserPublic.model_validate(current_user),
        global_completion=completion,
        lessons_done=lessons_done,
        exercises_passed=exercises_passed,
        projects_done=projects_done,
        quizzes_passed=quizzes_passed,
        badges=badges,
        recommendations=recommendations,
        last_lesson=last_lesson,
        weekly_goal={"target_minutes": 180, "done_minutes": min(180, lessons_done * 10), "message": "Continue avec une lecon courte aujourd'hui."},
        xp_to_next_level=xp_to_next_level(current_user.xp),
    )
