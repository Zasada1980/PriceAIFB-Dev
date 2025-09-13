#!/usr/bin/env python3
"""
Simple demo script to test Market Scout functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from market_scout.utils.database import init_db, SessionLocal
from market_scout.models import Listing, ProductCategory, ProductCondition
from market_scout.utils import extract_price, categorize_product
from market_scout.scrapers.yad2 import Yad2Scraper


def demo_utils():
    """Demonstrate utility functions."""
    print("=== Utility Functions Demo ===")
    
    # Price extraction
    test_prices = ["1500 שקל", "$2,000", "₪3500", "Price: 1,200"]
    for price_text in test_prices:
        price = extract_price(price_text)
        print(f"'{price_text}' -> {price}")
    
    print()
    
    # Product categorization
    test_products = [
        "Intel Core i7 מעבד",
        "NVIDIA RTX 3080 כרטיס מסך",
        "16GB DDR4 זיכרון",
        "מחשב גיימינג מלא"
    ]
    for product in test_products:
        category = categorize_product(product)
        print(f"'{product}' -> {category}")


def demo_database():
    """Demonstrate database functionality."""
    print("\n=== Database Demo ===")
    
    # Initialize database
    init_db()
    print("Database initialized")
    
    # Create sample listings
    db = SessionLocal()
    try:
        sample_listings = [
            Listing(
                title="Intel Core i7-12700K",
                description="מעבד גיימינג מצוין",
                price=1200.0,
                currency="ILS",
                category=ProductCategory.CPU,
                condition=ProductCondition.EXCELLENT,
                city="תל אביב",
                source_platform="demo",
                source_id="demo1"
            ),
            Listing(
                title="NVIDIA RTX 4070",
                description="כרטיס מסך חדש בקופסה",
                price=2800.0,
                currency="ILS",
                category=ProductCategory.GPU,
                condition=ProductCondition.NEW,
                city="חיפה",
                source_platform="demo",
                source_id="demo2"
            ),
            Listing(
                title="32GB DDR4 3200MHz",
                description="זיכרון למשחקים",
                price=400.0,
                currency="ILS",
                category=ProductCategory.RAM,
                condition=ProductCondition.GOOD,
                city="באר שבע",
                source_platform="demo",
                source_id="demo3"
            )
        ]
        
        # Check if demo data already exists
        existing = db.query(Listing).filter(Listing.source_platform == "demo").count()
        if existing == 0:
            db.add_all(sample_listings)
            db.commit()
            print(f"Added {len(sample_listings)} sample listings")
        else:
            print(f"Found {existing} existing demo listings")
        
        # Query data
        total = db.query(Listing).count()
        print(f"Total listings in database: {total}")
        
        # Show some listings
        recent = db.query(Listing).order_by(Listing.scraped_date.desc()).limit(3).all()
        print("\nRecent listings:")
        for listing in recent:
            print(f"  - {listing.title} | {listing.price} {listing.currency} | {listing.city}")
    
    finally:
        db.close()


def demo_scraper():
    """Demonstrate scraper functionality (without actually scraping)."""
    print("\n=== Scraper Demo ===")
    
    # Initialize scraper
    scraper = Yad2Scraper()
    print(f"Initialized {scraper.platform_name} scraper")
    
    # Test data parsing
    test_listing_data = {
        'title': 'Intel Core i5 מעבד למכירה',
        'description': 'מעבד במצב טוב, עובד מעולה',
        'price_text': '800 שקל',
        'location': 'תל אביב',
        'link': 'https://www.yad2.co.il/item/123456',
        'seller': 'יוסי כהן'
    }
    
    parsed = scraper.parse_listing(test_listing_data)
    if parsed:
        print("Parsed listing:")
        print(f"  Title: {parsed.title}")
        print(f"  Price: {parsed.price} {parsed.currency}")
        print(f"  Category: {parsed.category}")
        print(f"  Condition: {parsed.condition}")
        print(f"  City: {parsed.city}")
    else:
        print("Failed to parse test listing")


if __name__ == "__main__":
    print("Market Scout Israel - Demo Script")
    print("=" * 40)
    
    try:
        demo_utils()
        demo_database()
        demo_scraper()
        
        print("\n=== Demo Complete ===")
        print("To start the API server, run: python main.py serve")
        print("To scrape real data, run: python main.py scrape --query 'מחשב'")
        
    except Exception as e:
        print(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()