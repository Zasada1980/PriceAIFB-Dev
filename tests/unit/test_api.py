"""Test API endpoints."""

import pytest

from market_scout.models import Listing, ProductCategory, ProductCondition


class TestAPIEndpoints:
    """Test API functionality."""

    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Market Scout Israel API" in data["message"]

    def test_get_listings_empty(self, client):
        response = client.get("/listings")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_listings_with_data(self, client, db_session):
        # Create test listing
        listing = Listing(
            title="Test GPU",
            price=2000.0,
            currency="ILS",
            category=ProductCategory.GPU,
            condition=ProductCondition.GOOD,
            source_platform="test",
        )
        db_session.add(listing)
        db_session.commit()

        response = client.get("/listings")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test GPU"
        assert data[0]["price"] == 2000.0

    def test_get_listing_by_id(self, client, db_session):
        # Create test listing
        listing = Listing(
            title="Test CPU",
            price=1500.0,
            currency="ILS",
            category=ProductCategory.CPU,
            condition=ProductCondition.NEW,
            source_platform="test",
        )
        db_session.add(listing)
        db_session.commit()

        response = client.get(f"/listings/{listing.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test CPU"
        assert data["price"] == 1500.0

    def test_get_listing_not_found(self, client):
        response = client.get("/listings/999")
        assert response.status_code == 404

    def test_search_listings(self, client, db_session):
        # Create test listings
        listing1 = Listing(
            title="Intel CPU",
            price=1000.0,
            currency="ILS",
            category=ProductCategory.CPU,
            condition=ProductCondition.GOOD,
            source_platform="test",
        )
        listing2 = Listing(
            title="AMD GPU",
            price=2000.0,
            currency="ILS",
            category=ProductCategory.GPU,
            condition=ProductCondition.GOOD,
            source_platform="test",
        )
        db_session.add_all([listing1, listing2])
        db_session.commit()

        # Search for Intel
        response = client.get("/search?q=Intel")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Intel CPU"

        # Search for GPU
        response = client.get("/search?q=GPU")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "AMD GPU"

    def test_category_stats(self, client, db_session):
        # Create test listings
        listings = [
            Listing(
                title="CPU 1",
                price=1000.0,
                currency="ILS",
                category=ProductCategory.CPU,
                condition=ProductCondition.GOOD,
                source_platform="test",
            ),
            Listing(
                title="CPU 2",
                price=1500.0,
                currency="ILS",
                category=ProductCategory.CPU,
                condition=ProductCondition.GOOD,
                source_platform="test",
            ),
            Listing(
                title="GPU 1",
                price=2000.0,
                currency="ILS",
                category=ProductCategory.GPU,
                condition=ProductCondition.GOOD,
                source_platform="test",
            ),
        ]
        db_session.add_all(listings)
        db_session.commit()

        response = client.get("/stats/categories")
        assert response.status_code == 200
        data = response.json()

        # Should have stats for CPU and GPU
        assert len(data) == 2

        # Find CPU stats
        cpu_stats = next(item for item in data if item["category"] == "cpu")
        assert cpu_stats["count"] == 2
        assert cpu_stats["avg_price"] == 1250.0  # (1000 + 1500) / 2
        assert cpu_stats["min_price"] == 1000.0
        assert cpu_stats["max_price"] == 1500.0
