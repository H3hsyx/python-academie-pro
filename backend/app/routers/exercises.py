from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models import Exercise, ExerciseAttempt, User
from app.schemas import ExerciseAttemptCreate, ExerciseAttemptResult, ExercisePublic
from app.services.progress import add_xp, award_eligible_badges, mark_progress
from app.services.runner import grade_stdout, run_python_code

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("", response_model=list[ExercisePublic])
def list_exercises(
    level: str | None = None,
    theme: str | None = None,
    difficulty: str | None = None,
    exercise_type: str | None = None,
    q: str | None = None,
    limit: int = 60,
    db: Session = Depends(get_db),
) -> list[Exercise]:
    stmt = select(Exercise).order_by(Exercise.id).limit(min(limit, 200))
    if level:
        stmt = stmt.where(Exercise.level == level)
    if theme:
        stmt = stmt.where(Exercise.theme.ilike(f"%{theme}%"))
    if difficulty:
        stmt = stmt.where(Exercise.difficulty == difficulty)
    if exercise_type:
        stmt = stmt.where(Exercise.exercise_type == exercise_type)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(or_(Exercise.title.ilike(pattern), Exercise.description.ilike(pattern)))
    return list(db.scalars(stmt).all())


@router.get("/{exercise_id}", response_model=ExercisePublic)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)) -> Exercise:
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercice introuvable")
    return exercise


@router.post("/{exercise_id}/attempt", response_model=ExerciseAttemptResult)
def submit_attempt(
    exercise_id: int,
    payload: ExerciseAttemptCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> ExerciseAttemptResult:
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercice introuvable")
    output = run_python_code(payload.submitted_code)
    stdout = output.get("stdout", "") or ""
    stderr = output.get("stderr", "") or ""
    passed = not stderr and grade_stdout(stdout, exercise.expected_output)
    score = exercise.points if passed else 0
    attempt = ExerciseAttempt(
        user_id=current_user.id,
        exercise_id=exercise.id,
        submitted_code=payload.submitted_code,
        stdout=stdout,
        stderr=stderr,
        passed=passed,
        score=score,
    )
    db.add(attempt)
    awarded_xp = 0
    if passed:
        awarded_xp = exercise.points
        add_xp(current_user, awarded_xp)
        mark_progress(db, current_user, "exercise", exercise.id, 100)
        award_eligible_badges(db, current_user)
    db.commit()
    db.refresh(attempt)
    return ExerciseAttemptResult(
        id=attempt.id,
        passed=passed,
        score=score,
        stdout=stdout,
        stderr=stderr,
        expected_output=exercise.expected_output,
        explanation=exercise.explanation,
        awarded_xp=awarded_xp,
    )


@router.post("/run")
def run_code(payload: ExerciseAttemptCreate, current_user: Annotated[User, Depends(get_current_user)]):
    return run_python_code(payload.submitted_code)
