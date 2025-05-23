from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ModelHub"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./modelhub.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # À changer en production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 jours
    
    # Model Storage
    MODEL_STORAGE_PATH: str = "models"
    
    # Training Configuration
    MAX_WORKERS: int = 4
    BATCH_SIZE: int = 32
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 