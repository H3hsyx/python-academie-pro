from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.seed import seed_all
from app.db.session import SessionLocal, init_db
from app.routers import admin, auth, badges, community, courses, dashboard, exercises, profile, projects, quizzes, resources, search

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    if settings.seed_on_startup:
        with SessionLocal() as db:
            seed_all(db)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}


api_prefix = "/api"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(courses.router, prefix=api_prefix)
app.include_router(exercises.router, prefix=api_prefix)
app.include_router(quizzes.router, prefix=api_prefix)
app.include_router(projects.router, prefix=api_prefix)
app.include_router(dashboard.router, prefix=api_prefix)
app.include_router(profile.router, prefix=api_prefix)
app.include_router(community.router, prefix=api_prefix)
app.include_router(resources.router, prefix=api_prefix)
app.include_router(search.router, prefix=api_prefix)
app.include_router(badges.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)
