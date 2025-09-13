"""Tests for scoring service functionality."""

import pytest

from src.app.services.scoring import (
    ComponentSpecs,
    ScoringResult,
    ScoringService,
    create_demo_components,
)


class TestScoringService:
    """Test cases for the ScoringService class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scoring_service = ScoringService()

    def test_scoring_service_initialization(self):
        """Test that scoring service initializes correctly."""
        assert self.scoring_service.cpu_weight == 0.4
        assert self.scoring_service.gpu_weight == 0.5
        assert self.scoring_service.other_weight == 0.1
        assert self.scoring_service.vram_threshold == 8

    def test_calculate_rvi_basic(self):
        """Test basic RVI calculation."""
        components = ComponentSpecs(
            cpu_score=80.0,
            gpu_score=90.0,
            ram_gb=16,
            storage_gb=500,
            gpu_vram_gb=12,  # Above penalty threshold
            platform_score=1.0,
            liquidity_score=1.0,
            condition_score=1.0,
        )

        rvi = self.scoring_service.calculate_rvi(components)

        # Expected: (80 * 0.4 + 90 * 0.5 + ~50 * 0.1) * 1.0 * 1.0 * 1.0
        # = (32 + 45 + ~5) = ~82
        assert 80 <= rvi <= 85

    def test_calculate_rvi_with_vram_penalty(self):
        """Test RVI calculation with VRAM penalty applied."""
        components = ComponentSpecs(
            cpu_score=80.0,
            gpu_score=90.0,
            ram_gb=16,
            storage_gb=500,
            gpu_vram_gb=8,  # At penalty threshold
            platform_score=1.0,
            liquidity_score=1.0,
            condition_score=1.0,
        )

        rvi = self.scoring_service.calculate_rvi(components)

        # Should be reduced by penalty factor (0.85)
        # Base would be ~82, with penalty ~69.7
        assert 65 <= rvi <= 75

    def test_calculate_pvr(self):
        """Test PVR calculation."""
        rvi = 100.0
        price = 5000.0

        pvr = self.scoring_service.calculate_pvr(rvi, price)

        assert pvr == 0.02  # 100 / 5000

    def test_calculate_pvr_zero_price(self):
        """Test PVR calculation with zero price."""
        rvi = 100.0
        price = 0.0

        pvr = self.scoring_service.calculate_pvr(rvi, price)

        assert pvr == 0.0

    def test_score_listing_complete(self):
        """Test complete listing scoring."""
        components = ComponentSpecs(
            cpu_score=85.0,
            gpu_score=92.0,
            ram_gb=16,
            storage_gb=500,
            gpu_vram_gb=8,
            platform_score=1.1,
            liquidity_score=1.0,
            condition_score=0.9,
        )
        price = 4500.0

        result = self.scoring_service.score_listing(price, components)

        assert isinstance(result, ScoringResult)
        assert result.price == price
        assert result.components == components
        assert result.rvi > 0
        assert result.pvr > 0
        assert result.final_score > 0
        assert result.vram_penalty_applied is True  # 8GB triggers penalty

    def test_score_listing_invalid_price(self):
        """Test scoring with invalid price."""
        components = create_demo_components()

        with pytest.raises(ValueError, match="Price must be positive"):
            self.scoring_service.score_listing(-100.0, components)

    def test_scoring_result_to_dict(self):
        """Test ScoringResult serialization to dict."""
        components = ComponentSpecs(
            cpu_score=80.0,
            gpu_score=90.0,
            ram_gb=16,
            storage_gb=500,
        )

        result = ScoringResult(
            rvi=75.0,
            pvr=0.015,
            final_score=15.0,
            price=5000.0,
            components=components,
            vram_penalty_applied=False,
        )

        result_dict = result.to_dict()

        assert result_dict["rvi"] == 75.0
        assert result_dict["pvr"] == 0.015
        assert result_dict["final_score"] == 15.0
        assert result_dict["price"] == 5000.0
        assert result_dict["vram_penalty_applied"] is False
        assert "components" in result_dict
        assert result_dict["components"]["cpu_score"] == 80.0

    def test_create_demo_components(self):
        """Test demo components creation."""
        demo_components = create_demo_components()

        assert isinstance(demo_components, ComponentSpecs)
        assert demo_components.cpu_score > 0
        assert demo_components.gpu_score > 0
        assert demo_components.ram_gb > 0
        assert demo_components.storage_gb > 0
        assert demo_components.gpu_vram_gb > 0

    def test_edge_case_high_ram_storage(self):
        """Test edge case with very high RAM and storage."""
        components = ComponentSpecs(
            cpu_score=100.0,
            gpu_score=100.0,
            ram_gb=128,  # Very high
            storage_gb=4000,  # Very high
            gpu_vram_gb=24,
            platform_score=1.0,
            liquidity_score=1.0,
            condition_score=1.0,
        )

        rvi = self.scoring_service.calculate_rvi(components)

        # Other score should be capped at 100
        # Expected: (100 * 0.4 + 100 * 0.5 + 100 * 0.1) = 100
        assert 95 <= rvi <= 100

    def test_rvi_calculation_weights_sum_to_one(self):
        """Test that weights sum to 1.0 for proper normalization."""
        total_weight = (
            self.scoring_service.cpu_weight
            + self.scoring_service.gpu_weight
            + self.scoring_service.other_weight
        )

        assert abs(total_weight - 1.0) < 0.001  # Allow small floating point error
