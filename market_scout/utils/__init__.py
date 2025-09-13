"""Utility functions and helpers."""

import re
import random
import time
from typing import Optional
from market_scout.config import settings


def extract_price(text: str) -> Optional[float]:
    """Extract price from text string."""
    if not text:
        return None

    # Remove common currency symbols and thousands separators
    cleaned = re.sub(r"[₪$€,]", "", text)

    # Look for price patterns
    price_patterns = [
        r"(\d+(?:\.\d{1,2})?)",  # Simple number
        r"(\d+(?:,\d{3})*(?:\.\d{1,2})?)",  # Number with thousands separator
    ]

    for pattern in price_patterns:
        match = re.search(pattern, cleaned)
        if match:
            try:
                price_str = match.group(1).replace(",", "")
                return float(price_str)
            except ValueError:
                continue

    return None


def extract_city(text: str) -> Optional[str]:
    """Extract city name from text."""
    if not text:
        return None

    # Common Israeli cities
    cities = [
        "תל אביב",
        "חיפה",
        "ירושלים",
        "באר שבע",
        "נתניה",
        "פתח תקווה",
        "אשדוד",
        "רישון לציון",
        "אשקלון",
        "רעננה",
        "רמת גן",
        "הרצליה",
        "כפר סבא",
        "חולון",
        "בת ים",
        "רמלה",
        "Tel Aviv",
        "Haifa",
        "Jerusalem",
        "Beer Sheva",
        "Netanya",
        "Petah Tikva",
    ]

    text_lower = text.lower()
    for city in cities:
        if city.lower() in text_lower:
            return city

    return None


def random_delay():
    """Add random delay between requests."""
    delay = random.uniform(settings.scraping_delay_min, settings.scraping_delay_max)
    time.sleep(delay)


def normalize_text(text: str) -> str:
    """Normalize text for consistent processing."""
    if not text:
        return ""

    # Remove extra whitespace
    text = " ".join(text.split())

    # Remove special characters but keep Hebrew/English/numbers
    text = re.sub(r"[^\w\s\u0590-\u05FF]", " ", text)

    return text.strip()


def categorize_product(title: str, description: str = "") -> str:
    """Automatically categorize product based on title and description."""
    text = f"{title} {description}".lower()

    categories = {
        "cpu": ["cpu", "processor", "מעבד", "intel", "amd", "ryzen", "core"],
        "gpu": [
            "gpu",
            "graphics",
            "video card",
            "כרטיס מסך",
            "nvidia",
            "amd",
            "rtx",
            "gtx",
        ],
        "motherboard": ["motherboard", "לוח אם", "mobo", "mb"],
        "ram": ["ram", "memory", "זיכרון", "ddr4", "ddr5", "gb"],
        "storage": ["ssd", "hdd", "storage", "אחסון", "hard drive", "nvme"],
        "psu": ["psu", "power supply", "ספק כוח", "power"],
        "cooling": ["cooling", "cooler", "fan", "קירור", "radiator"],
        "case": ["case", "chassis", "מארז", "tower"],
        "complete_build": ["מחשב", "computer", "pc", "build", "מורכב"],
    }

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "other"
