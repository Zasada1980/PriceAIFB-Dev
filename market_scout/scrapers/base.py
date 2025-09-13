"""Base scraper interface and common functionality."""

import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
from market_scout.config import settings
from market_scout.models import ListingCreate, ProductCondition
from market_scout.utils import random_delay


logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base scraper class for all platform scrapers."""

    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": settings.user_agent})

    @abstractmethod
    def search_listings(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """Search for listings on the platform."""
        pass

    @abstractmethod
    def parse_listing(self, listing_data: Dict[str, Any]) -> Optional[ListingCreate]:
        """Parse a single listing into standardized format."""
        pass

    def scrape_listings(self, query: str, max_pages: int = 5) -> List[ListingCreate]:
        """Scrape listings from the platform."""
        all_listings = []

        try:
            raw_listings = self.search_listings(query, max_pages=max_pages)

            for raw_listing in raw_listings:
                try:
                    parsed_listing = self.parse_listing(raw_listing)
                    if parsed_listing:
                        all_listings.append(parsed_listing)
                except Exception as e:
                    logger.error(f"Error parsing listing: {e}")
                    continue

                random_delay()

        except Exception as e:
            logger.error(f"Error scraping {self.platform_name}: {e}")

        return all_listings

    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """Get BeautifulSoup object for URL."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def normalize_condition(self, condition_text: str) -> ProductCondition:
        """Normalize condition text to standard condition enum."""
        if not condition_text:
            return ProductCondition.GOOD

        condition_text = condition_text.lower()

        if any(word in condition_text for word in ["חדש", "new", "brand new"]):
            return ProductCondition.NEW
        elif any(
            word in condition_text for word in ["כמו חדש", "like new", "excellent"]
        ):
            return ProductCondition.LIKE_NEW
        elif any(word in condition_text for word in ["מצוין", "excellent"]):
            return ProductCondition.EXCELLENT
        elif any(word in condition_text for word in ["טוב", "good"]):
            return ProductCondition.GOOD
        elif any(word in condition_text for word in ["סביר", "fair", "average"]):
            return ProductCondition.FAIR
        elif any(word in condition_text for word in ["גרוע", "poor", "bad"]):
            return ProductCondition.POOR
        elif any(word in condition_text for word in ["חלקים", "parts", "broken"]):
            return ProductCondition.FOR_PARTS

        return ProductCondition.GOOD  # Default
