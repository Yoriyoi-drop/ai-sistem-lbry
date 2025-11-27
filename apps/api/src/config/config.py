"""
Configuration settings for Infinite AI Security Platform
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from datetime import timedelta


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Infinite AI Security Platform"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")  # No default to force environment variable
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable must be set")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./infinite_ai_security.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]  # In production, be more restrictive
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Security Scanning
    DEFAULT_SCAN_TIMEOUT: int = 300  # seconds
    MAX_CONCURRENT_SCANS: int = 10
    SCAN_RESULT_RETENTION_DAYS: int = 30
    
    # Agent Management
    AGENT_HEARTBEAT_INTERVAL: int = 30  # seconds
    AGENT_TIMEOUT_THRESHOLD: int = 90  # seconds
    
    # Labyrinth Configuration
    LABYRINTH_ENABLED: bool = True
    LABYRINTH_DEFENSE_LEVEL: str = "moderate"  # low, moderate, high, extreme
    
    # External Services
    N8N_URL: str = os.getenv("N8N_URL", "http://localhost:5678")
    SCANNER_GO_URL: str = os.getenv("SCANNER_GO_URL", "http://localhost:8080")
    LABYRINTH_RUST_URL: str = os.getenv("LABYRINTH_RUST_URL", "http://localhost:8081")
    
    # Feature Flags
    ENABLE_USER_REGISTRATION: bool = True
    ENABLE_SUBSCRIPTIONS: bool = True
    ENABLE_ENTERPRISE_FEATURES: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()