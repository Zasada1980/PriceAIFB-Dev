"""Main pipeline runner for demonstrating scoring functionality."""

import json
import sys
from typing import Any

from ..core.logging import get_logger
from ..services.scoring import ScoringService, create_demo_components

logger = get_logger(__name__)


def run_demo_pipeline() -> dict[str, Any]:
    """
    Run a demo scoring pipeline with sample data.

    Returns:
        Dict containing demo results in JSON format
    """
    logger.info("Starting demo scoring pipeline")

    # Initialize scoring service
    scoring_service = ScoringService()

    # Create demo components
    demo_components = create_demo_components()

    # Demo price (in local currency, e.g., ILS)
    demo_price = 4500.0

    logger.info(
        "Demo listing details",
        price=demo_price,
        cpu_score=demo_components.cpu_score,
        gpu_score=demo_components.gpu_score,
        ram_gb=demo_components.ram_gb,
        storage_gb=demo_components.storage_gb,
        gpu_vram_gb=demo_components.gpu_vram_gb,
    )

    # Score the demo listing
    try:
        result = scoring_service.score_listing(
            price=demo_price, components=demo_components
        )

        # Create output result
        demo_result = {
            "status": "success",
            "pipeline": "demo_scoring",
            "timestamp": "2024-01-01T12:00:00Z",  # Would be datetime.utcnow() in real implementation
            "input": {
                "price": demo_price,
                "description": "Demo Gaming PC - Intel i5-12400F, RTX 3070, 16GB RAM, 500GB SSD",
            },
            "scoring": result.to_dict(),
            "interpretation": {
                "investment_grade": (
                    "good"
                    if result.final_score > 15
                    else "average" if result.final_score > 10 else "poor"
                ),
                "recommendation": _get_recommendation(result),
                "profit_potential": (
                    f"{((result.rvi / demo_price) - 1) * 100:.1f}%"
                    if result.rvi > demo_price
                    else "N/A"
                ),
            },
        }

        logger.info(
            "Demo pipeline completed successfully",
            final_score=result.final_score,
            investment_grade=demo_result["interpretation"]["investment_grade"],  # type: ignore[index]
        )

        return demo_result

    except Exception as e:
        logger.error("Demo pipeline failed", error=str(e), exc_info=True)
        return {
            "status": "error",
            "pipeline": "demo_scoring",
            "error": str(e),
            "timestamp": "2024-01-01T12:00:00Z",
        }


def _get_recommendation(result) -> str:
    """Get investment recommendation based on scoring result."""
    if result.final_score > 20:
        return "🔥 Excellent deal - strong buy recommendation"
    elif result.final_score > 15:
        return "✅ Good investment opportunity"
    elif result.final_score > 10:
        return "⚠️ Average deal - consider other factors"
    else:
        return "❌ Poor value - avoid or negotiate significantly"


def main():
    """Main entry point for demo pipeline."""
    logger.info("PriceAIFB-Dev Demo Pipeline Starting")

    try:
        # Run demo pipeline
        result = run_demo_pipeline()

        # Output JSON result
        json_output = json.dumps(result, indent=2, ensure_ascii=False)
        print(json_output)

        # Log completion
        logger.info("Demo pipeline execution completed")

        # Exit with appropriate code
        sys.exit(0 if result.get("status") == "success" else 1)

    except Exception as e:
        logger.error("Pipeline execution failed", error=str(e), exc_info=True)
        error_result = {"status": "error", "pipeline": "demo_scoring", "error": str(e)}
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
