from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Agentic Beginner"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    GOOGLE_API_KEY: str = Field(default="", repr=False)
    GEMINI_MODEL: str = "gemini-2.5-flash"

    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/agentic_beginner"

    VECTOR_STORE_PROVIDER: str = "chroma"
    CHROMA_PERSIST_DIRECTORY: str = "data/processed/chroma"
    PGVECTOR_COLLECTION_NAME: str = "agentic_knowledge_base"

    ALLOWED_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://localhost:8501",
            "http://127.0.0.1:8501",
        ]
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
