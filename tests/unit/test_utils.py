"""Test utility functions."""

import pytest

from market_scout.utils import (
    categorize_product,
    extract_city,
    extract_price,
    normalize_text,
)


class TestExtractPrice:
    """Test price extraction functionality."""

    def test_extract_simple_price(self):
        assert extract_price("1500") == 1500.0
        assert extract_price("1500.50") == 1500.5

    def test_extract_price_with_currency(self):
        assert extract_price("₪1500") == 1500.0
        assert extract_price("$1500") == 1500.0
        assert extract_price("1500₪") == 1500.0

    def test_extract_price_with_thousands_separator(self):
        assert extract_price("1,500") == 1500.0
        assert extract_price("15,000") == 15000.0

    def test_extract_price_from_text(self):
        assert extract_price("מחיר: 1500 שקל") == 1500.0
        assert extract_price("Price: $1,500") == 1500.0

    def test_extract_price_invalid(self):
        assert extract_price("") is None
        assert extract_price("no price here") is None
        assert extract_price(None) is None


class TestExtractCity:
    """Test city extraction functionality."""

    def test_extract_hebrew_cities(self):
        assert extract_city("תל אביב") == "תל אביב"
        assert extract_city("נמצא בחיפה") == "חיפה"
        assert extract_city("ירושלים בלבד") == "ירושלים"

    def test_extract_english_cities(self):
        assert extract_city("Tel Aviv") == "Tel Aviv"
        assert extract_city("Located in Haifa") == "Haifa"

    def test_extract_city_case_insensitive(self):
        assert extract_city("tel aviv") == "Tel Aviv"
        assert extract_city("HAIFA") == "Haifa"

    def test_extract_city_not_found(self):
        assert extract_city("unknown location") is None
        assert extract_city("") is None
        assert extract_city(None) is None


class TestCategorizeProduct:
    """Test product categorization functionality."""

    def test_categorize_cpu(self):
        assert categorize_product("Intel Core i7") == "cpu"
        assert categorize_product("AMD Ryzen 5") == "cpu"
        assert categorize_product("מעבד אינטל") == "cpu"

    def test_categorize_gpu(self):
        assert categorize_product("NVIDIA RTX 3080") == "gpu"
        assert categorize_product("כרטיס מסך") == "gpu"
        assert categorize_product("Graphics Card") == "gpu"

    def test_categorize_ram(self):
        assert categorize_product("16GB DDR4 RAM") == "ram"
        assert categorize_product("זיכרון 32GB") == "ram"
        assert categorize_product("Memory 8GB") == "ram"

    def test_categorize_storage(self):
        assert categorize_product("SSD 1TB") == "storage"
        assert categorize_product("Hard Drive 2TB") == "storage"
        assert categorize_product("NVMe SSD") == "storage"

    def test_categorize_complete_build(self):
        assert categorize_product("מחשב גיימינג") == "complete_build"
        assert categorize_product("Gaming PC") == "complete_build"
        assert categorize_product("Computer Build") == "complete_build"

    def test_categorize_unknown(self):
        assert categorize_product("some random text") == "other"
        assert categorize_product("") == "other"


class TestNormalizeText:
    """Test text normalization functionality."""

    def test_normalize_whitespace(self):
        assert normalize_text("  hello   world  ") == "hello world"
        assert normalize_text("hello\n\nworld") == "hello world"
        assert normalize_text("hello\t\tworld") == "hello world"

    def test_normalize_special_chars(self):
        text = "hello!@#$%^&*()world"
        result = normalize_text(text)
        assert "hello" in result
        assert "world" in result

    def test_normalize_hebrew(self):
        assert normalize_text("שלום עולם") == "שלום עולם"
        assert normalize_text("  שלום   עולם  ") == "שלום עולם"

    def test_normalize_empty(self):
        assert normalize_text("") == ""
        assert normalize_text(None) == ""
