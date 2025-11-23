from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI-Based Remedial Class Scheduler"
    environment: str = "development"
    # Supabase PostgreSQL connection (pooler mode on port 6543)
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
    openai_api_key: str | None = None
    google_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
