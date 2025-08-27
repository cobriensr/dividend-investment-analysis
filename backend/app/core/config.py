import secrets
from typing import Any, Dict, List, Optional, Union
from functools import lru_cache
from pydantic import AnyHttpUrl, Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Dividend Investment Analysis"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for analyzing dividend investments and portfolio management"

    # Security
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database
    DATABASE_URL: Optional[str] = Field(None, env="DATABASE_URL")
    POSTGRES_SERVER: str = Field(default="localhost", env="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(default="postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="dividend_db", env="POSTGRES_DB")

    # Build DATABASE_URL if not provided
    @field_validator("DATABASE_URL", pre=True)
    def assemble_db_connection(self, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(self, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # External API Keys (for fetching stock/dividend data)
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    POLYGON_API_KEY: Optional[str] = None
    IEX_CLOUD_API_KEY: Optional[str] = None
    YAHOO_FINANCE_API_KEY: Optional[str] = None

    # Email (for notifications)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # Redis (for caching stock prices)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Testing
    TESTING: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"

    # Features
    ENABLE_CACHE: bool = True
    CACHE_TTL: int = 300  # 5 minutes

    # Cache configuration
    CACHE_PROVIDER: str = "dynamodb"  # or "redis" or "memory"
    CACHE_TTL_SECONDS: int = 300  # 5 minutes

    # DynamoDB
    DYNAMODB_TABLE: str = "dividend-cache"
    AWS_REGION: str = "us-east-1"

    class Config:
        env_file = ".env"
        case_sensitive = True

        # Allow extra fields during validation
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """
    Create cached settings instance
    Use this to avoid reading .env file multiple times
    """
    return Settings()


# Create a single instance
settings = get_settings()


# Email templates
class EmailTemplates:
    WELCOME_SUBJECT = "Welcome to Dividend Investment Analysis"
    RESET_PASSWORD_SUBJECT = "Password Reset Request"
    DIVIDEND_ALERT_SUBJECT = "Dividend Payment Alert"


# Stock market constants
class MarketConfig:
    MARKET_OPEN_HOUR = 9
    MARKET_OPEN_MINUTE = 30
    MARKET_CLOSE_HOUR = 16
    MARKET_CLOSE_MINUTE = 0
    TIMEZONE = "America/New_York"

    # Dividend aristocrats minimum years
    ARISTOCRAT_YEARS = 25

    # Portfolio constraints
    MAX_PORTFOLIO_SIZE = 100
    MIN_POSITION_SIZE = 0.01  # 1% minimum
    MAX_POSITION_SIZE = 0.25  # 25% maximum
