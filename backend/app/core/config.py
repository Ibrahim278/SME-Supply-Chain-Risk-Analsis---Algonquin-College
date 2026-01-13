"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://sme:password@localhost:5432/sme"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # MinIO (S3-compatible storage)
    MINIO_URL: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "sme-files"

    # LLM Configuration
    LLM_PROVIDER: str = "openai"  # openai | anthropic | google
    LLM_MODEL: str = "gpt-4o"
    LLM_API_KEY: str = ""

    # JWT Authentication
    JWT_SECRET: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Logging
    LOG_LEVEL: str = "INFO"

    # Debug
    DEBUG: bool = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Singleton instance for convenience
settings = get_settings()
