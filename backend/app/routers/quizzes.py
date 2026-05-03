from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models import Quiz, QuizResult, User
from app.schemas import QuizPublic, QuizResultPublic, QuizSubmit
from app.services.progress import add_xp, award_eligible_badges, mark_progress

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


def public_quiz(quiz: Quiz) -> QuizPublic:
    return QuizPublic(
        id=quiz.id,
        module_id=quiz.module_id,
        lesson_id=quiz.lesson_id,
        title=quiz.title,
        description=quiz.description,
        difficulty=quiz.difficulty,
        time_limit_minutes=quiz.time_limit_minutes,
        questions=[
            {"id": item.id, "question": item.question, "question_type": item.question_type, "options": item.options, "points": item.points}
            for item in quiz.questions
        ],
    )


def normalize_answer(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip().lower()
    return value


@router.get("/{quiz_id}", response_model=QuizPublic)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)) -> QuizPublic:
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz introuvable")
    return public_quiz(quiz)


@router.post("/{quiz_id}/submit", response_model=QuizResultPublic)
def submit_quiz(
    quiz_id: int,
    payload: QuizSubmit,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> QuizResultPublic:
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz introuvable")
    total = sum(q.points for q in quiz.questions)
    score = 0
    corrections: list[dict[str, Any]] = []
    for question in quiz.questions:
        given = payload.answers.get(str(question.id))
        correct = question.correct_answer
        ok = normalize_answer(given) == normalize_answer(correct)
        if ok:
            score += question.points
        corrections.append(
            {
                "question_id": question.id,
                "ok": ok,
                "given": given,
                "correct_answer": correct,
                "explanation": question.explanation,
            }
        )
    passed = total > 0 and score / total >= 0.7
    result = QuizResult(user_id=current_user.id, quiz_id=quiz.id, score=score, total=total, passed=passed, answers=payload.answers)
    db.add(result)
    awarded_xp = 0
    if passed:
        awarded_xp = 20
        add_xp(current_user, awarded_xp)
        mark_progress(db, current_user, "quiz", quiz.id, 100)
        award_eligible_badges(db, current_user)
    db.commit()
    db.refresh(result)
    return QuizResultPublic(
        id=result.id,
        score=score,
        total=total,
        passed=passed,
        answers=payload.answers,
        created_at=result.created_at,
        corrections=corrections,
        awarded_xp=awarded_xp,
    )
