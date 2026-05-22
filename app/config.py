import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/relayhive"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # FastAPI
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"
    API_V1_PREFIX: str = "/v1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Work Order Configuration
    MAX_RELAY_CHAIN_DEPTH: int = 10
    WORK_ORDER_RETENTION_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
