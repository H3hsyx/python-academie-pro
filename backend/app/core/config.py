from __future__ import annotations

from functools import lru_cache
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Python Academie Pro"
    environment: str = "development"
    database_url: str = "sqlite:///./python_academie.db"
    secret_key: str = "change-me-with-openssl-rand-hex-32"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    backend_cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    seed_on_startup: bool = True
    enable_code_execution: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def split_cors(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
