import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./subscription_service.db")
    
    # Security settings
    SECRET_KEY: str = os.getenv("SUBSCRIPTION_SECRET_KEY")  # No default to force environment variable
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SECRET_KEY:
            raise ValueError("SUBSCRIPTION_SECRET_KEY environment variable must be set")
    
    # Stripe settings (for payment processing)
    STRIPE_SECRET_KEY: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET: Optional[str] = os.getenv("STRIPE_WEBHOOK_SECRET")
    STRIPE_API_VERSION: str = "2023-10-16"
    
    # Email settings
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: Optional[int] = int(os.getenv("SMTP_PORT", 587)) if os.getenv("SMTP_PORT") else 587
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: Optional[str] = os.getenv("EMAILS_FROM_EMAIL")
    
    # System settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Infinite AI Security - Subscription Service"
    BACKEND_CORS_ORIGINS: list = []
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        case_sensitive = True


settings = Settings()