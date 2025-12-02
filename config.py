"""
Configuration management for Python services
"""
import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_secret_key: str = os.getenv("API_SECRET_KEY")  # No default value to force environment variable
    api_debug: bool = os.getenv("API_DEBUG", "false").lower() == "true"
    api_workers: int = int(os.getenv("API_WORKERS", "1"))
    api_version: str = os.getenv("API_VERSION", "v1")

    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/infinite_ai_security")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    database_echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"

    # Redis Configuration
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_password: Optional[str] = os.getenv("REDIS_PASSWORD")
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_db: int = int(os.getenv("REDIS_DB", "0"))

    # Authentication Configuration
    api_secret_key: Optional[str] = os.getenv("API_SECRET_KEY")  # No default value to force environment variable
    jwt_secret_key: Optional[str] = os.getenv("JWT_SECRET_KEY")  # No default value to force environment variable
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    jwt_refresh_token_expire_minutes: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", "43200"))
    password_hash_algorithm: str = os.getenv("PASSWORD_HASH_ALGORITHM", "bcrypt")
    password_min_length: int = int(os.getenv("PASSWORD_MIN_LENGTH", "8"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate critical configuration values (only in production/debug mode)
        if self.api_debug == "false" or os.getenv("FORCE_STRICT_CONFIG", "false").lower() == "true":
            if not self.api_secret_key:
                raise ValueError("API_SECRET_KEY environment variable must be set")
            if not self.jwt_secret_key:
                raise ValueError("JWT_SECRET_KEY environment variable must be set")

    # AI Services Configuration
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")

    # Security Configuration
    cors_origins: list = Field(default_factory=lambda: os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(","))
    security_password_min_length: int = int(os.getenv("SECURITY_PASSWORD_MIN_LENGTH", "8"))
    security_password_require_symbol: bool = os.getenv("SECURITY_PASSWORD_REQUIRE_SYMBOL", "false").lower() == "true"
    security_password_require_number: bool = os.getenv("SECURITY_PASSWORD_REQUIRE_NUMBER", "true").lower() == "true"
    security_password_require_uppercase: bool = os.getenv("SECURITY_PASSWORD_REQUIRE_UPPERCASE", "true").lower() == "true"
    security_password_require_lowercase: bool = os.getenv("SECURITY_PASSWORD_REQUIRE_LOWERCASE", "true").lower() == "true"

    # Rate Limiting
    rate_limit_default: int = int(os.getenv("RATE_LIMIT_DEFAULT", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/app.log")
    log_format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # File Upload
    max_upload_size: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))
    allowed_file_extensions: list = Field(default_factory=lambda: os.getenv("ALLOWED_FILE_EXTENSIONS", "txt,pdf,py,js,go,rs,ts,tsx,jsx,json,yml,yaml").split(","))
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads/")

    # External Services
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN")
    slack_webhook_url: Optional[str] = os.getenv("SLACK_WEBHOOK_URL")
    discord_webhook_url: Optional[str] = os.getenv("DISCORD_WEBHOOK_URL")

    # Sentry (Error Tracking)
    sentry_dsn: Optional[str] = os.getenv("SENTRY_DSN")

    # Email Configuration
    email_host: str = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    email_port: int = int(os.getenv("EMAIL_PORT", "587"))
    email_username: Optional[str] = os.getenv("EMAIL_USERNAME")
    email_password: Optional[str] = os.getenv("EMAIL_PASSWORD")
    email_from: Optional[str] = os.getenv("EMAIL_FROM")

    # Monitoring
    prometheus_enabled: bool = os.getenv("PROMETHEUS_ENABLED", "true").lower() == "true"
    grafana_url: str = os.getenv("GRAFANA_URL", "http://localhost:3000")
    metrics_enabled: bool = os.getenv("METRICS_ENABLED", "true").lower() == "true"

    # Feature Flags
    enable_ai_agents: bool = os.getenv("ENABLE_AI_AGENTS", "true").lower() == "true"
    enable_security_scanner: bool = os.getenv("ENABLE_SECURITY_SCANNER", "true").lower() == "true"
    enable_labyrinth: bool = os.getenv("ENABLE_LABYRINTH", "true").lower() == "true"
    enable_huggingface: bool = False  # Hugging Face support has been removed, using Ollama instead
    enable_real_time_updates: bool = os.getenv("ENABLE_REAL_TIME_UPDATES", "true").lower() == "true"
    enable_user_registration: bool = os.getenv("ENABLE_USER_REGISTRATION", "true").lower() == "true"
    enable_email_verification: bool = os.getenv("ENABLE_EMAIL_VERIFICATION", "true").lower() == "true"

    # Ollama Configuration
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_security_model: str = os.getenv("OLLAMA_SECURITY_MODEL", "qwen:7b-instruct")
    ollama_timeout: int = int(os.getenv("OLLAMA_TIMEOUT", "300"))
    ai_engine_type: str = os.getenv("AI_ENGINE_TYPE", "ollama")  # rust, ollama, openai, anthropic

    # Scanner Configuration
    scanner_timeout: int = int(os.getenv("SCANNER_TIMEOUT", "30"))
    scanner_max_file_size: int = int(os.getenv("SCANNER_MAX_FILE_SIZE", "5242880"))
    scanner_supported_languages: list = Field(default_factory=lambda: os.getenv("SCANNER_SUPPORTED_LANGUAGES", "python,javascript,go,rust,typescript").split(","))

    # Labyrinth Configuration
    labyrinth_complexity: str = os.getenv("LABYRINTH_COMPLEXITY", "medium")
    labyrinth_timeout: int = int(os.getenv("LABYRINTH_TIMEOUT", "60"))
    labyrinth_max_depth: int = int(os.getenv("LABYRINTH_MAX_DEPTH", "100"))

    # Testing Configuration
    testing: bool = os.getenv("TESTING", "false").lower() == "true"
    test_database_url: str = os.getenv("TEST_DATABASE_URL", "postgresql://user:password@localhost:5432/infinite_ai_security_test")

    # Web3 Configuration (Optional)
    web3_enabled: bool = os.getenv("WEB3_ENABLED", "false").lower() == "true"
    web3_rpc_url: str = os.getenv("WEB3_RPC_URL", "https://mainnet.infura.io/v3/YOUR-PROJECT-ID")
    web3_contract_address: str = os.getenv("WEB3_CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")

    # Subscription Service Configuration
    stripe_secret_key: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    stripe_publishable_key: Optional[str] = os.getenv("STRIPE_PUBLISHABLE_KEY")
    stripe_webhook_secret: Optional[str] = os.getenv("STRIPE_WEBHOOK_SECRET")
    subscription_enabled: bool = os.getenv("SUBSCRIPTION_ENABLED", "true").lower() == "true"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"  # Ignore extra fields to avoid validation errors
    }


# Global settings instance
settings = Settings()