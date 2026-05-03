from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class APIMessage(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: str
    level: str
    xp: int
    streak_days: int
    avatar_url: str | None = None
    created_at: datetime
    last_login: datetime | None = None


class CoursePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    level: str
    track_type: str
    order_index: int
    estimated_duration: str
    objectives: list[str]
    final_projects: list[str]


class ModulePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    title: str
    description: str
    level: str
    order_index: int
    estimated_duration: str


class LessonListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    module_id: int
    slug: str
    title: str
    order_index: int
    difficulty: str
    summary: str


class LessonDetail(LessonListItem):
    content: str
    code_examples: list[dict[str, Any]]
    objectives: list[str]
    common_errors: list[str]
    tips: list[str]
    mini_exercise: dict[str, Any]


class ExercisePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lesson_id: int | None = None
    slug: str
    title: str
    description: str
    starter_code: str
    expected_output: str
    solution: str
    optimized_solution: str
    explanation: str
    difficulty: str
    level: str
    theme: str
    duration_minutes: int
    exercise_type: str
    hints: list[str]
    tests: list[dict[str, Any]]
    points: int


class ExerciseAttemptCreate(BaseModel):
    submitted_code: str = Field(min_length=1)


class ExerciseAttemptResult(BaseModel):
    id: int
    passed: bool
    score: int
    stdout: str
    stderr: str
    expected_output: str
    explanation: str
    awarded_xp: int


class QuizQuestionPublic(BaseModel):
    id: int
    question: str
    question_type: str
    options: list[str]
    points: int


class QuizPublic(BaseModel):
    id: int
    module_id: int | None = None
    lesson_id: int | None = None
    title: str
    description: str
    difficulty: str
    time_limit_minutes: int
    questions: list[QuizQuestionPublic]


class QuizSubmit(BaseModel):
    answers: dict[str, Any]


class QuizResultPublic(BaseModel):
    id: int
    score: int
    total: int
    passed: bool
    answers: dict[str, Any]
    created_at: datetime
    corrections: list[dict[str, Any]] = []
    awarded_xp: int = 0


class ProjectPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    level: str
    category: str
    estimated_duration: str
    objective: str
    skills: list[str]
    difficulty: str


class ProjectDetail(ProjectPublic):
    specifications: str
    steps: list[str]
    starter_code: str
    hints: list[str]
    final_code: str
    improvements: list[str]
    bonus: str


class ProjectSubmissionCreate(BaseModel):
    repository_url: str | None = None
    notes: str = ""


class ProjectSubmissionPublic(BaseModel):
    id: int
    project_id: int
    status: str
    repository_url: str | None
    notes: str
    created_at: datetime
    awarded_xp: int = 0


class BadgePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    title: str
    description: str
    icon: str
    xp_required: int
    rule_type: str
    rule_value: int


class UserBadgePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    awarded_at: datetime
    badge: BadgePublic


class UserProgressPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    entity_type: str
    entity_id: int
    status: str
    percent: int
    completed_at: datetime | None
    updated_at: datetime


class FavoriteCreate(BaseModel):
    entity_type: str
    entity_id: int


class FavoritePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    entity_type: str
    entity_id: int
    created_at: datetime


class CommentCreate(BaseModel):
    entity_type: str
    entity_id: int
    content: str = Field(min_length=2)
    parent_id: int | None = None


class CommentPublic(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    parent_id: int | None
    content: str
    created_at: datetime
    username: str


class DiscussionCreate(BaseModel):
    title: str = Field(min_length=3)
    body: str = Field(min_length=5)
    theme: str = "general"


class DiscussionPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    title: str
    slug: str
    body: str
    theme: str
    pinned: bool
    solved: bool
    created_at: datetime


class ResourceItemPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    kind: str
    level: str
    content: str
    tags: list[str]


class ChallengePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    description: str
    level: str
    theme: str
    duration_minutes: int
    starter_code: str
    solution: str
    tests: list[dict[str, Any]]
    points: int


class DashboardStats(BaseModel):
    user: UserPublic
    global_completion: int
    lessons_done: int
    exercises_passed: int
    projects_done: int
    quizzes_passed: int
    badges: list[UserBadgePublic]
    recommendations: list[LessonListItem]
    last_lesson: LessonListItem | None = None
    weekly_goal: dict[str, Any]
    xp_to_next_level: int


class SearchResult(BaseModel):
    entity_type: str
    entity_id: int
    title: str
    description: str
    url: str
    level: str | None = None
