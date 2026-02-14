# core/config.py
# Configuration management using pydantic-settings

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./kopu.db"
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Agent API Key
    AGENT_API_KEY: str = "your-agent-api-key-here"
    
    # Application
    APP_NAME: str = "Backend API"

    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # CORS - Allow all origins for development (including file:// protocol)
    CORS_ORIGINS: str = "*"


    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )



settings = Settings()


def get_database_url() -> str:
    """Get the database URL, using SQLite as fallback for development."""
    return settings.DATABASE_URL


def is_postgresql() -> bool:
    """Check if using PostgreSQL."""
    return settings.DATABASE_URL.startswith("postgresql")
