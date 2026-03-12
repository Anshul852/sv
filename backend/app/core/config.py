from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    APP_NAME: str = "ScholarMind"
    DEBUG: bool = True
    
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_KEY")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    ADMIN_TOKEN: str = os.getenv("ADMIN_TOKEN", "admin-dev-token")
    
    CORS_ORIGINS: List[str] = ["*"]
    
    MICROSOFT_CLIENT_ID: Optional[str] = os.getenv("MICROSOFT_CLIENT_ID")
    MICROSOFT_CLIENT_SECRET: Optional[str] = os.getenv("MICROSOFT_CLIENT_SECRET")
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
