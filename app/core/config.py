"""Application configuration using environment variables."""

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Stores configuration values for the application."""

    db_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/cardvault"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()
