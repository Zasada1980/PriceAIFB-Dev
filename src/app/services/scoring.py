"""Scoring service for calculating RVI (Resale Value Index) and PVR (Price-to-Value Ratio)."""

from dataclasses import dataclass

from ..core.config import settings
from ..core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ComponentSpecs:
    """Component specifications for scoring."""

    cpu_score: float = 0.0
    gpu_score: float = 0.0
    ram_gb: int = 0
    storage_gb: int = 0
    gpu_vram_gb: int = 0

    # Platform and condition factors
    platform_score: float = 1.0  # Upgrade potential
    liquidity_score: float = 1.0  # Market liquidity
    condition_score: float = 1.0  # Condition and warranty


@dataclass
class ScoringResult:
    """Result of scoring calculation."""

    rvi: float
    pvr: float
    final_score: float
    price: float
    components: ComponentSpecs
    vram_penalty_applied: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "rvi": self.rvi,
            "pvr": self.pvr,
            "final_score": self.final_score,
            "price": self.price,
            "vram_penalty_applied": self.vram_penalty_applied,
            "components": {
                "cpu_score": self.components.cpu_score,
                "gpu_score": self.components.gpu_score,
                "ram_gb": self.components.ram_gb,
                "storage_gb": self.components.storage_gb,
                "gpu_vram_gb": self.components.gpu_vram_gb,
                "platform_score": self.components.platform_score,
                "liquidity_score": self.components.liquidity_score,
                "condition_score": self.components.condition_score,
            },
        }


class ScoringService:
    """Service for calculating listing scores using RVI and PVR metrics."""

    def __init__(self):
        self.cpu_weight = settings.cpu_weight
        self.gpu_weight = settings.gpu_weight
        self.other_weight = settings.other_weight
        self.vram_threshold = settings.vram_penalty_threshold
        self.vram_penalty = settings.vram_penalty_factor

        logger.info(
            "ScoringService initialized",
            cpu_weight=self.cpu_weight,
            gpu_weight=self.gpu_weight,
            other_weight=self.other_weight,
            vram_threshold=self.vram_threshold,
        )

    def calculate_rvi(self, components: ComponentSpecs) -> float:
        """
        Calculate RVI (Resale Value Index).

        Formula: RVI = (CPU_score × wCPU + GPU_score × wGPU + Other_score × wOther)
                      × PLS × MLI × CWM × VRAM_penalty
        """
        # Normalize other components score (RAM + Storage)
        other_score = min(
            (components.ram_gb / 32.0) * 50 + (components.storage_gb / 1000.0) * 50,
            100.0,
        )

        # Base RVI calculation
        base_rvi = (
            components.cpu_score * self.cpu_weight
            + components.gpu_score * self.gpu_weight
            + other_score * self.other_weight
        )

        # Apply multipliers
        rvi = (
            base_rvi
            * components.platform_score  # PLS - Platform Liquidity Score
            * components.liquidity_score  # MLI - Market Liquidity Index
            * components.condition_score  # CWM - Condition/Warranty Multiplier
        )

        # Apply VRAM penalty if applicable
        vram_penalty_applied = False
        if components.gpu_vram_gb > 0 and components.gpu_vram_gb <= self.vram_threshold:
            rvi *= self.vram_penalty
            vram_penalty_applied = True
            logger.debug(
                "VRAM penalty applied",
                gpu_vram_gb=components.gpu_vram_gb,
                penalty_factor=self.vram_penalty,
            )

        logger.debug(
            "RVI calculated",
            base_rvi=base_rvi,
            final_rvi=rvi,
            other_score=other_score,
            vram_penalty_applied=vram_penalty_applied,
        )

        return rvi

    def calculate_pvr(self, rvi: float, price: float) -> float:
        """
        Calculate PVR (Price-to-Value Ratio).

        PVR = RVI / Price (higher is better for buyers)
        """
        if price <= 0:
            logger.warning("Invalid price for PVR calculation", price=price)
            return 0.0

        pvr = rvi / price
        logger.debug("PVR calculated", rvi=rvi, price=price, pvr=pvr)
        return pvr

    def score_listing(self, price: float, components: ComponentSpecs) -> ScoringResult:
        """
        Score a complete listing with RVI and PVR calculations.

        Args:
            price: Listing price
            components: Component specifications

        Returns:
            ScoringResult with all calculated metrics
        """
        logger.info(
            "Scoring listing",
            price=price,
            cpu_score=components.cpu_score,
            gpu_score=components.gpu_score,
        )

        # Validate inputs
        if price <= 0:
            raise ValueError(f"Price must be positive, got: {price}")

        # Calculate RVI
        rvi = self.calculate_rvi(components)

        # Calculate PVR
        pvr = self.calculate_pvr(rvi, price)

        # Final deal score (normalized PVR for comparison)
        final_score = pvr * 1000  # Scale for readability

        # Check if VRAM penalty was applied
        vram_penalty_applied = (
            components.gpu_vram_gb > 0 and components.gpu_vram_gb <= self.vram_threshold
        )

        result = ScoringResult(
            rvi=rvi,
            pvr=pvr,
            final_score=final_score,
            price=price,
            components=components,
            vram_penalty_applied=vram_penalty_applied,
        )

        logger.info(
            "Listing scored",
            rvi=rvi,
            pvr=pvr,
            final_score=final_score,
            vram_penalty_applied=vram_penalty_applied,
        )

        return result


def create_demo_components() -> ComponentSpecs:
    """Create demo component specifications for testing."""
    return ComponentSpecs(
        cpu_score=85.0,  # Example: Intel i5-12400F
        gpu_score=92.0,  # Example: RTX 3070
        ram_gb=16,
        storage_gb=500,  # SSD
        gpu_vram_gb=8,  # RTX 3070 VRAM
        platform_score=1.1,  # Good upgrade potential
        liquidity_score=1.0,  # Standard liquidity
        condition_score=0.9,  # Good condition, some warranty
    )
