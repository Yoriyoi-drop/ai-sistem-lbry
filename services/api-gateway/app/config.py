"""
Configuration loader for Infinite AI Security Platform
Loads environment variables and provides typed configuration objects
"""
import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file from project root
# config.py is in services/api-gateway/app/config.py
# We need to go up 4 levels to reach root
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
env_path = os.path.join(root_dir, '.env')
print(f"DEBUG: Loading .env from {env_path}")
load_dotenv(env_path)
print(f"DEBUG: JWT_SECRET_KEY present: {'JWT_SECRET_KEY' in os.environ}")
print(f"DEBUG: JWT_SECRET_KEY value: {os.getenv('JWT_SECRET_KEY')}")

@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str
    pool_size: int = 20
    max_overflow: int = 10
    echo: bool = False
    
    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        return cls(
            url=os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5436/ai_security"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "20")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
            echo=os.getenv("DB_ECHO", "false").lower() == "true"
        )

@dataclass
class RedisConfig:
    """Redis configuration"""
    url: str
    max_connections: int = 50
    decode_responses: bool = True
    
    @classmethod
    def from_env(cls) -> "RedisConfig":
        return cls(
            url=os.getenv("REDIS_URL", "redis://localhost:6383"),
            max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "50")),
            decode_responses=os.getenv("REDIS_DECODE_RESPONSES", "true").lower() == "true"
        )

@dataclass
class JWTConfig:
    """JWT configuration"""
    secret_key: str
    refresh_secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    
    @classmethod
    def from_env(cls) -> "JWTConfig":
        secret = os.getenv("JWT_SECRET_KEY")
        if not secret:
            raise ValueError("JWT_SECRET_KEY must be set in environment")
        
        refresh_secret = os.getenv("JWT_REFRESH_SECRET")
        if not refresh_secret:
            raise ValueError("JWT_REFRESH_SECRET must be set in environment")
            
        return cls(
            secret_key=secret,
            refresh_secret=refresh_secret,
            algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")),
            refresh_token_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        )

@dataclass
class ServiceConfig:
    """External service URLs"""
    ai_hub_url: str
    scanner_url: str
    labyrinth_url: str
    
    @classmethod
    def from_env(cls) -> "ServiceConfig":
        return cls(
            ai_hub_url=os.getenv("AI_HUB_URL", "http://localhost:8031"),
            scanner_url=os.getenv("SCANNER_URL", "http://localhost:8032"),
            labyrinth_url=os.getenv("LABYRINTH_URL", "http://localhost:8033")
        )

@dataclass
class SecurityConfig:
    """Security configuration"""
    max_request_size: int = 5 * 1024 * 1024  # 5MB
    rate_limit_per_minute: int = 60
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 15
    password_min_length: int = 12
    
    @classmethod
    def from_env(cls) -> "SecurityConfig":
        return cls(
            max_request_size=int(os.getenv("MAX_REQUEST_SIZE", str(5 * 1024 * 1024))),
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_RPM", "60")),
            max_login_attempts=int(os.getenv("MAX_LOGIN_ATTEMPTS", "5")),
            lockout_duration_minutes=int(os.getenv("LOCKOUT_DURATION_MINUTES", "15")),
            password_min_length=int(os.getenv("PASSWORD_MIN_LENGTH", "12"))
        )

@dataclass
class AppConfig:
    """Main application configuration"""
    environment: str
    debug: bool
    host: str
    port: int
    database: DatabaseConfig
    redis: RedisConfig
    jwt: JWTConfig
    services: ServiceConfig
    security: SecurityConfig
    openai_api_key: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            database=DatabaseConfig.from_env(),
            redis=RedisConfig.from_env(),
            jwt=JWTConfig.from_env(),
            services=ServiceConfig.from_env(),
            security=SecurityConfig.from_env(),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        return self.environment == "development"

# Global config instance
config = AppConfig.from_env()
