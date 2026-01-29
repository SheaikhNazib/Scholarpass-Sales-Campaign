from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import json

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str
    DATABASE_ECHO: bool
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    
    # Redis Configuration
    REDIS_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    
    # JWT Configuration
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_HOURS: int
    
    # Application Configuration
    PORT: int
    DEBUG: bool
    ENVIRONMENT: str
    SERVER_HOST: str
    SERVER_PORT: int
    
    # CORS Configuration
    CORS_ORIGINS: List[str]
    
    # Database Auto Migration
    DB_AUTO_MIGRATE: bool

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
