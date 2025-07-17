from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Base configuration
    APP_NAME: str = "CReddit"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "creddit"

    # Security
    SECRET_KEY: str = "your-secret-key-keep-it-safe"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
