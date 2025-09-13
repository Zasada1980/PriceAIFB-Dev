"""Test configuration and fixtures for PriceAIFB-Dev."""

import pytest


@pytest.fixture
def sample_components():
    """Sample component specifications for testing."""
    from src.app.services.scoring import ComponentSpecs

    return ComponentSpecs(
        cpu_score=85.0,
        gpu_score=90.0,
        ram_gb=16,
        storage_gb=500,
        gpu_vram_gb=8,
        platform_score=1.0,
        liquidity_score=1.0,
        condition_score=1.0,
    )


@pytest.fixture
def scoring_service():
    """Scoring service instance for testing."""
    from src.app.services.scoring import ScoringService

    return ScoringService()
