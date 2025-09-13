"""Configuration management for Market Scout Israel."""

from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Database Configuration
    database_url: str = Field(default="sqlite:///market_scout.db")

    # Scraping Configuration
    scraping_delay_min: int = Field(default=1)
    scraping_delay_max: int = Field(default=3)
    max_concurrent_requests: int = Field(default=5)
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )

    # API Configuration
    api_host: str = Field(default="localhost")
    api_port: int = Field(default=8000)
    api_debug: bool = Field(default=False)

    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Platform Configuration
    facebook_groups: List[str] = Field(default_factory=list)
    yad2_base_url: str = Field(default="https://www.yad2.co.il")

    # Data Management
    data_retention_days: int = Field(default=365)


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


# Global settings instance
settings = get_settings()
