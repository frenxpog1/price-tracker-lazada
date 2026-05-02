"""
Configuration management for the E-commerce Price Tracker application.
Loads settings from environment variables with sensible defaults.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "E-commerce Price Tracker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://dev_user:dev_password@localhost:5432/price_tracker_dev"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Google OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    # SMTP Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    # CORS - can be a JSON string or list
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # Scraping
    SCRAPER_TIMEOUT: int = 10  # seconds
    SCRAPER_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Monitoring
    PRICE_CHECK_INTERVAL_HOURS: int = 24
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            # Parse CORS_ORIGINS if it's a JSON string
            if field_name == 'CORS_ORIGINS':
                if isinstance(raw_val, str) and raw_val.startswith('['):
                    return json.loads(raw_val)
            return raw_val


# Global settings instance
settings = Settings()
