from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Advanced RAG"
    environment: str = "development"
    database_url: str
    pinecone_api_key: str | None = None
    pinecone_index_name: str = "advanced-rag"
    openai_api_key: str | None = None

    @field_validator("pinecone_api_key", "openai_api_key", mode="before")
    @classmethod
    def normalize_optional_keys(cls, value: object) -> object:
        """Treat missing or whitespace-only API keys as unset."""
        if isinstance(value, str) and not value.strip():
            return None
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
