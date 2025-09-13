"""Yad2 scraper for computer components."""

import re
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from market_scout.scrapers.base import BaseScraper
from market_scout.models import ListingCreate, ProductCategory
from market_scout.config import settings
from market_scout.utils import (
    extract_price,
    extract_city,
    normalize_text,
    categorize_product,
)


logger = logging.getLogger(__name__)


class Yad2Scraper(BaseScraper):
    """Scraper for Yad2 platform."""

    def __init__(self):
        super().__init__("yad2")
        self.base_url = settings.yad2_base_url

    def search_listings(self, query: str, max_pages: int = 5) -> List[Dict[str, Any]]:
        """Search for computer component listings on Yad2."""
        listings = []

        # Yad2 search URL for computers category
        search_url = f"{self.base_url}/computers"

        for page in range(1, max_pages + 1):
            try:
                soup = self.get_soup(search_url)
                if not soup:
                    break

                # Find listing containers (this may need adjustment based on Yad2's structure)
                listing_elements = soup.find_all(
                    "div", class_=re.compile(r"feeditem|item|listing")
                )

                if not listing_elements:
                    logger.warning(f"No listings found on page {page}")
                    break

                for element in listing_elements:
                    listing_data = self._extract_listing_data(element)
                    if listing_data:
                        listings.append(listing_data)

                logger.info(
                    f"Scraped page {page}, found {len(listing_elements)} listings"
                )

            except Exception as e:
                logger.error(f"Error scraping Yad2 page {page}: {e}")
                break

        return listings

    def _extract_listing_data(self, element) -> Optional[Dict[str, Any]]:
        """Extract listing data from HTML element."""
        try:
            # Extract title
            title_elem = element.find(
                ["h2", "h3", "a"], class_=re.compile(r"title|link")
            )
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract price
            price_elem = element.find(class_=re.compile(r"price"))
            price_text = price_elem.get_text(strip=True) if price_elem else ""

            # Extract location
            location_elem = element.find(class_=re.compile(r"location|city"))
            location = location_elem.get_text(strip=True) if location_elem else ""

            # Extract description
            desc_elem = element.find(class_=re.compile(r"description|content"))
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            # Extract link
            link_elem = element.find("a", href=True)
            link = urljoin(self.base_url, link_elem["href"]) if link_elem else ""

            # Extract seller info
            seller_elem = element.find(class_=re.compile(r"seller|author"))
            seller = seller_elem.get_text(strip=True) if seller_elem else ""

            if not title or not price_text:
                return None

            return {
                "title": title,
                "description": description,
                "price_text": price_text,
                "location": location,
                "link": link,
                "seller": seller,
                "raw_element": str(element),  # For debugging
            }

        except Exception as e:
            logger.error(f"Error extracting listing data: {e}")
            return None

    def parse_listing(self, listing_data: Dict[str, Any]) -> Optional[ListingCreate]:
        """Parse Yad2 listing into standardized format."""
        try:
            title = normalize_text(listing_data.get("title", ""))
            description = normalize_text(listing_data.get("description", ""))

            # Extract price
            price = extract_price(listing_data.get("price_text", ""))
            if not price:
                return None

            # Extract location
            city = extract_city(listing_data.get("location", ""))

            # Categorize product
            category = categorize_product(title, description)

            # Extract source ID from URL if available
            source_id = None
            link = listing_data.get("link", "")
            if link:
                parsed_url = urlparse(link)
                if parsed_url.path:
                    # Try to extract ID from path
                    path_parts = parsed_url.path.split("/")
                    for part in reversed(path_parts):
                        if part.isdigit():
                            source_id = part
                            break

            return ListingCreate(
                title=title,
                description=description,
                price=price,
                currency="ILS",
                category=ProductCategory(category),
                condition=self.normalize_condition(description),
                city=city,
                seller_name=listing_data.get("seller", ""),
                source_platform="yad2",
                source_url=link,
                source_id=source_id,
            )

        except Exception as e:
            logger.error(f"Error parsing Yad2 listing: {e}")
            return None
