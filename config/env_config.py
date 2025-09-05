from functools import lru_cache
from typing import Optional, Dict
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    APP_NAME: str = "Bio Krystal"
    DEBUG: bool = False

    # Fullscript keys
    FULLSCRIPT_CLIENT_ID: Optional[str] = None
    FULLSCRIPT_CLIENT_SECRET: Optional[str] = None
    FULLSCRIPT_REDIRECT_URI: Optional[str] = None
    FULLSCRIPT_API_URL: Optional[str] = None

    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Logging
    LOG_LEVEL: str = "INFO"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    # Env
    ENVIRONMENT: str = "development"

    # Google Cloud/Project
    GOOGLE_API_KEY: Optional[str] = None
    GCP_PROJECT_ID: Optional[str] = None
    GCP_LOCATION: Optional[str] = None

    # JWT/Auth
    JWT_KEY: Optional[str] = None
    ALGORITHM: Optional[str] = None
    ACCESS_KEY_EXPIRE_DAYS: Optional[int] = None

    # Cloud Storage
    CLOUD_STORAGE_BUCKET_NAME: Optional[str] = None

    # SendGrid
    SENDGRID_API_KEY: Optional[str] = None

    # Frontend
    FRONTEND_RESET_PASSWORD_URL: str = "https://frontend-333120675205.us-central1.run.app/reset-password"
    FRONTEND_PATIENT_RESET_PASSWORD_URL: str = "https://frontend-333120675205.us-central1.run.app/patient_reset_password"
    FRONTEND_PATIENT_SET_PASSWORD_URL: str = "http://localhost:3000/patient_set_password"

    # Firestore
    FIRESTORE_CREDENTIALS_JSON: Optional[str] = None
    
    class Config:
        env_file = f".env.{os.getenv('ENV', 'development')}"
        case_sensitive = True

@lru_cache()
def get_settings():
    environment = os.getenv("ENVIRONMENT", "development")
    settings = Settings(ENVIRONMENT=environment)
    if settings.ENVIRONMENT.lower() == "production":
        settings.DEBUG = False
        settings.LOG_LEVEL = "INFO"
        if isinstance(settings.CORS_ORIGINS, str):
            cors_str = settings.CORS_ORIGINS.strip('"').strip("'")
            if cors_str == "*":
                settings.CORS_ORIGINS = []
            else:
                settings.CORS_ORIGINS = [origin.strip() for origin in cors_str.split(",") if origin.strip()]
        else:
            settings.CORS_ORIGINS = []
        settings.CORS_HEADERS = [
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "X-Requested-With"
        ]
    else:
        settings.DEBUG = True
        settings.LOG_LEVEL = "INFO"
        settings.CORS_ORIGINS = ["*"]
    return settings

settings = get_settings()
