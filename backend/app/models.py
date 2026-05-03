from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="user", nullable=False)
    level: Mapped[str] = mapped_column(String(80), default="Debutant", nullable=False)
    xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streak_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    attempts: Mapped[list[ExerciseAttempt]] = relationship(back_populates="user", cascade="all, delete-orphan")
    quiz_results: Mapped[list[QuizResult]] = relationship(back_populates="user", cascade="all, delete-orphan")
    badges: Mapped[list[UserBadge]] = relationship(back_populates="user", cascade="all, delete-orphan")
    progress_items: Mapped[list[UserProgress]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    track_type: Mapped[str] = mapped_column(String(100), default="general", index=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_duration: Mapped[str] = mapped_column(String(80), default="8 semaines")
    objectives: Mapped[list[str]] = mapped_column(JSON, default=list)
    final_projects: Mapped[list[str]] = mapped_column(JSON, default=list)

    modules: Mapped[list[Module]] = relationship(back_populates="course", cascade="all, delete-orphan", order_by="Module.order_index")


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_duration: Mapped[str] = mapped_column(String(80), default="3 h")

    course: Mapped[Course] = relationship(back_populates="modules")
    lessons: Mapped[list[Lesson]] = relationship(back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order_index")
    quizzes: Mapped[list[Quiz]] = relationship(back_populates="module", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    code_examples: Mapped[list[dict]] = mapped_column(JSON, default=list)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(60), default="facile", index=True)
    objectives: Mapped[list[str]] = mapped_column(JSON, default=list)
    common_errors: Mapped[list[str]] = mapped_column(JSON, default=list)
    tips: Mapped[list[str]] = mapped_column(JSON, default=list)
    mini_exercise: Mapped[dict] = mapped_column(JSON, default=dict)
    summary: Mapped[str] = mapped_column(Text, default="")

    module: Mapped[Module] = relationship(back_populates="lessons")
    exercises: Mapped[list[Exercise]] = relationship(back_populates="lesson", cascade="all, delete-orphan")
    quizzes: Mapped[list[Quiz]] = relationship(back_populates="lesson", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int | None] = mapped_column(ForeignKey("lessons.id", ondelete="SET NULL"), index=True, nullable=True)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    starter_code: Mapped[str] = mapped_column(Text, default="")
    expected_output: Mapped[str] = mapped_column(Text, default="")
    solution: Mapped[str] = mapped_column(Text, default="")
    optimized_solution: Mapped[str] = mapped_column(Text, default="")
    explanation: Mapped[str] = mapped_column(Text, default="")
    difficulty: Mapped[str] = mapped_column(String(60), default="facile", index=True)
    level: Mapped[str] = mapped_column(String(80), default="Debutant", index=True)
    theme: Mapped[str] = mapped_column(String(120), default="Python", index=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=10)
    exercise_type: Mapped[str] = mapped_column(String(80), default="ecrire une fonction", index=True)
    hints: Mapped[list[str]] = mapped_column(JSON, default=list)
    tests: Mapped[list[dict]] = mapped_column(JSON, default=list)
    points: Mapped[int] = mapped_column(Integer, default=10)

    lesson: Mapped[Lesson | None] = relationship(back_populates="exercises")
    attempts: Mapped[list[ExerciseAttempt]] = relationship(back_populates="exercise", cascade="all, delete-orphan")


class ExerciseAttempt(Base):
    __tablename__ = "exercise_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id", ondelete="CASCADE"), index=True)
    submitted_code: Mapped[str] = mapped_column(Text, nullable=False)
    stdout: Mapped[str] = mapped_column(Text, default="")
    stderr: Mapped[str] = mapped_column(Text, default="")
    passed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="attempts")
    exercise: Mapped[Exercise] = relationship(back_populates="attempts")


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int | None] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True, nullable=True)
    lesson_id: Mapped[int | None] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    difficulty: Mapped[str] = mapped_column(String(60), default="facile")
    time_limit_minutes: Mapped[int] = mapped_column(Integer, default=8)

    module: Mapped[Module | None] = relationship(back_populates="quizzes")
    lesson: Mapped[Lesson | None] = relationship(back_populates="quizzes")
    questions: Mapped[list[QuizQuestion]] = relationship(back_populates="quiz", cascade="all, delete-orphan")
    results: Mapped[list[QuizResult]] = relationship(back_populates="quiz", cascade="all, delete-orphan")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(60), default="qcm")
    options: Mapped[list[str]] = mapped_column(JSON, default=list)
    correct_answer: Mapped[object] = mapped_column(JSON, default=dict)
    explanation: Mapped[str] = mapped_column(Text, default="")
    points: Mapped[int] = mapped_column(Integer, default=1)

    quiz: Mapped[Quiz] = relationship(back_populates="questions")


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), index=True)
    score: Mapped[int] = mapped_column(Integer, default=0)
    total: Mapped[int] = mapped_column(Integer, default=0)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="quiz_results")
    quiz: Mapped[Quiz] = relationship(back_populates="results")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    estimated_duration: Mapped[str] = mapped_column(String(80), default="4 h")
    objective: Mapped[str] = mapped_column(Text, default="")
    skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    specifications: Mapped[str] = mapped_column(Text, default="")
    steps: Mapped[list[str]] = mapped_column(JSON, default=list)
    starter_code: Mapped[str] = mapped_column(Text, default="")
    hints: Mapped[list[str]] = mapped_column(JSON, default=list)
    final_code: Mapped[str] = mapped_column(Text, default="")
    improvements: Mapped[list[str]] = mapped_column(JSON, default=list)
    bonus: Mapped[str] = mapped_column(Text, default="")
    difficulty: Mapped[str] = mapped_column(String(60), default="moyen")

    submissions: Mapped[list[ProjectSubmission]] = relationship(back_populates="project", cascade="all, delete-orphan")


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    repository_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(60), default="submitted", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    project: Mapped[Project] = relationship(back_populates="submissions")
    user: Mapped[User] = relationship()


class Badge(Base):
    __tablename__ = "badges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(String(80), default="award")
    xp_required: Mapped[int] = mapped_column(Integer, default=0)
    rule_type: Mapped[str] = mapped_column(String(80), default="xp")
    rule_value: Mapped[int] = mapped_column(Integer, default=0)

    users: Mapped[list[UserBadge]] = relationship(back_populates="badge", cascade="all, delete-orphan")


class UserBadge(Base):
    __tablename__ = "user_badges"
    __table_args__ = (UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    badge_id: Mapped[int] = mapped_column(ForeignKey("badges.id", ondelete="CASCADE"), index=True)
    awarded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="badges")
    badge: Mapped[Badge] = relationship(back_populates="users")


class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (UniqueConstraint("user_id", "entity_type", "entity_id", name="uq_user_progress_entity"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    entity_type: Mapped[str] = mapped_column(String(40), index=True)
    entity_id: Mapped[int] = mapped_column(Integer, index=True)
    status: Mapped[str] = mapped_column(String(40), default="started", index=True)
    percent: Mapped[int] = mapped_column(Integer, default=0)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user: Mapped[User] = relationship(back_populates="progress_items")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    entity_type: Mapped[str] = mapped_column(String(50), index=True)
    entity_id: Mapped[int] = mapped_column(Integer, index=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id"), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped[User] = relationship()


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "entity_type", "entity_id", name="uq_favorite_entity"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    entity_type: Mapped[str] = mapped_column(String(50), index=True)
    entity_id: Mapped[int] = mapped_column(Integer, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped[User] = relationship()


class Discussion(Base):
    __tablename__ = "discussions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    theme: Mapped[str] = mapped_column(String(120), index=True, default="general")
    pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    solved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped[User] = relationship()


class ResourceItem(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    kind: Mapped[str] = mapped_column(String(80), index=True, default="memo")
    level: Mapped[str] = mapped_column(String(80), index=True, default="Tous niveaux")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    theme: Mapped[str] = mapped_column(String(120), index=True, default="Algorithmique")
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    starter_code: Mapped[str] = mapped_column(Text, default="")
    solution: Mapped[str] = mapped_column(Text, default="")
    tests: Mapped[list[dict]] = mapped_column(JSON, default=list)
    points: Mapped[int] = mapped_column(Integer, default=40)


class ChallengeAttempt(Base):
    __tablename__ = "challenge_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id", ondelete="CASCADE"), index=True)
    submitted_code: Mapped[str] = mapped_column(Text, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
