"""Configuration management for Market Scout Israel."""

import os
from typing import List, Optional
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///market_scout.db", env="DATABASE_URL")
    
    # Scraping Configuration
    scraping_delay_min: int = Field(default=1, env="SCRAPING_DELAY_MIN")
    scraping_delay_max: int = Field(default=3, env="SCRAPING_DELAY_MAX")
    max_concurrent_requests: int = Field(default=5, env="MAX_CONCURRENT_REQUESTS")
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        env="USER_AGENT"
    )
    
    # API Configuration
    api_host: str = Field(default="localhost", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_debug: bool = Field(default=False, env="API_DEBUG")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Platform Configuration
    facebook_groups: List[str] = Field(default_factory=list, env="FACEBOOK_GROUPS")
    yad2_base_url: str = Field(default="https://www.yad2.co.il", env="YAD2_BASE_URL")
    
    # Data Management
    data_retention_days: int = Field(default=365, env="DATA_RETENTION_DAYS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


# Global settings instance
settings = get_settings()