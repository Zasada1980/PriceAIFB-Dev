"""Configuration management with Pydantic Settings."""


from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    app_name: str = Field(default="PriceAIFB-Dev", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")

    # Database
    database_url: str = Field(
        default="sqlite:///priceaifb.db", description="Database connection URL"
    )

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")

    # Scoring parameters
    cpu_weight: float = Field(default=0.4, description="CPU weight in RVI calculation")
    gpu_weight: float = Field(default=0.5, description="GPU weight in RVI calculation")
    other_weight: float = Field(
        default=0.1, description="Other components weight in RVI"
    )

    # Platform and liquidation factors
    platform_score_base: float = Field(default=1.0, description="Base platform score")
    liquidity_score_base: float = Field(default=1.0, description="Base liquidity score")
    condition_score_base: float = Field(default=1.0, description="Base condition score")

    # VRAM penalty threshold
    vram_penalty_threshold: int = Field(
        default=8, description="VRAM GB threshold for penalty"
    )
    vram_penalty_factor: float = Field(
        default=0.85, description="VRAM penalty multiplier"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
