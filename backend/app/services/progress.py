from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Badge, ExerciseAttempt, ProjectSubmission, QuizResult, User, UserBadge, UserProgress

LEVELS = [
    (0, "Debutant"),
    (150, "Apprenti Python"),
    (500, "Codeur junior"),
    (1200, "Developpeur intermediaire"),
    (2500, "Developpeur confirme"),
    (5000, "Expert Python"),
]


def compute_level(xp: int) -> str:
    current = LEVELS[0][1]
    for threshold, name in LEVELS:
        if xp >= threshold:
            current = name
    return current


def xp_to_next_level(xp: int) -> int:
    for threshold, _ in LEVELS:
        if xp < threshold:
            return threshold - xp
    return 0


def add_xp(user: User, amount: int) -> None:
    user.xp += max(0, amount)
    user.level = compute_level(user.xp)


def mark_progress(db: Session, user: User, entity_type: str, entity_id: int, percent: int = 100) -> UserProgress:
    item = db.scalar(
        select(UserProgress).where(
            UserProgress.user_id == user.id,
            UserProgress.entity_type == entity_type,
            UserProgress.entity_id == entity_id,
        )
    )
    now = datetime.now(timezone.utc)
    if item is None:
        item = UserProgress(user_id=user.id, entity_type=entity_type, entity_id=entity_id)
        db.add(item)
    item.percent = max(item.percent or 0, percent)
    item.status = "completed" if item.percent >= 100 else "started"
    item.completed_at = now if item.status == "completed" and item.completed_at is None else item.completed_at
    item.updated_at = now
    return item


def award_eligible_badges(db: Session, user: User) -> list[UserBadge]:
    existing = {row.badge_id for row in db.scalars(select(UserBadge).where(UserBadge.user_id == user.id)).all()}
    badges = db.scalars(select(Badge)).all()
    awarded: list[UserBadge] = []

    lessons_done = db.scalar(
        select(func.count(UserProgress.id)).where(
            UserProgress.user_id == user.id,
            UserProgress.entity_type == "lesson",
            UserProgress.status == "completed",
        )
    ) or 0
    exercises_passed = db.scalar(
        select(func.count(ExerciseAttempt.id)).where(ExerciseAttempt.user_id == user.id, ExerciseAttempt.passed.is_(True))
    ) or 0
    projects_done = db.scalar(
        select(func.count(ProjectSubmission.id)).where(
            ProjectSubmission.user_id == user.id,
            ProjectSubmission.status.in_(["submitted", "accepted"]),
        )
    ) or 0
    quizzes_passed = db.scalar(
        select(func.count(QuizResult.id)).where(QuizResult.user_id == user.id, QuizResult.passed.is_(True))
    ) or 0

    for badge in badges:
        if badge.id in existing:
            continue
        ok = False
        if badge.rule_type == "xp":
            ok = user.xp >= badge.rule_value
        elif badge.rule_type == "lessons_done":
            ok = lessons_done >= badge.rule_value
        elif badge.rule_type == "exercises_passed":
            ok = exercises_passed >= badge.rule_value
        elif badge.rule_type == "projects_done":
            ok = projects_done >= badge.rule_value
        elif badge.rule_type == "quizzes_passed":
            ok = quizzes_passed >= badge.rule_value
        if ok:
            user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
            db.add(user_badge)
            awarded.append(user_badge)
    return awarded
