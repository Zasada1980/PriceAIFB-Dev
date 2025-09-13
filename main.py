"""Command line interface for Market Scout Israel."""

import click
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from market_scout.utils.database import SessionLocal, init_db
from market_scout.models import Listing
from market_scout.scrapers.yad2 import Yad2Scraper
from market_scout.scrapers.facebook import FacebookGroupsScraper
from market_scout.config import settings


# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=settings.log_format
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Market Scout Israel CLI."""
    pass


@cli.command()
def init_database():
    """Initialize the database."""
    click.echo("Initializing database...")
    init_db()
    click.echo("Database initialized successfully!")


@cli.command()
@click.option('--query', default='מחשב', help='Search query')
@click.option('--pages', default=3, help='Number of pages to scrape')
@click.option('--platform', default='yad2', help='Platform to scrape (yad2, facebook)')
def scrape(query, pages, platform):
    """Scrape listings from a platform."""
    click.echo(f"Scraping {platform} for '{query}' ({pages} pages)...")
    
    db = SessionLocal()
    try:
        if platform == 'yad2':
            scraper = Yad2Scraper()
            listings = scraper.scrape_listings(query, max_pages=pages)
        elif platform == 'facebook':
            if not settings.facebook_groups:
                click.echo("No Facebook groups configured. Please set FACEBOOK_GROUPS environment variable.")
                return
            scraper = FacebookGroupsScraper(settings.facebook_groups)
            listings = scraper.scrape_all_groups(query)
        else:
            click.echo(f"Unknown platform: {platform}")
            return
        
        # Save listings to database
        saved_count = 0
        for listing_data in listings:
            try:
                # Check if listing already exists
                existing = db.query(Listing).filter(
                    Listing.source_platform == listing_data.source_platform,
                    Listing.source_id == listing_data.source_id
                ).first()
                
                if not existing:
                    listing = Listing(**listing_data.dict())
                    db.add(listing)
                    saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving listing: {e}")
        
        db.commit()
        click.echo(f"Found {len(listings)} listings, saved {saved_count} new ones.")
        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        db.rollback()
    finally:
        db.close()


@cli.command()
@click.option('--category', help='Filter by category')
@click.option('--city', help='Filter by city')
@click.option('--limit', default=10, help='Number of listings to show')
def list_listings(category, city, limit):
    """List recent listings."""
    db = SessionLocal()
    try:
        query = db.query(Listing)
        
        if category:
            query = query.filter(Listing.category == category)
        if city:
            query = query.filter(Listing.city.ilike(f"%{city}%"))
        
        listings = query.order_by(Listing.scraped_date.desc()).limit(limit).all()
        
        click.echo(f"Found {len(listings)} listings:")
        for listing in listings:
            click.echo(f"- {listing.title} | {listing.price} {listing.currency} | {listing.city or 'Unknown'} | {listing.category}")
            
    finally:
        db.close()


@cli.command()
def stats():
    """Show database statistics."""
    db = SessionLocal()
    try:
        total_listings = db.query(Listing).count()
        platforms = db.query(Listing.source_platform).distinct().all()
        categories = db.query(Listing.category).distinct().all()
        
        click.echo(f"Total listings: {total_listings}")
        click.echo(f"Platforms: {', '.join([p[0] for p in platforms])}")
        click.echo(f"Categories: {', '.join([c[0] for c in categories])}")
        
        # Recent activity
        recent = db.query(Listing).filter(
            Listing.scraped_date >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        click.echo(f"Listings added today: {recent}")
        
    finally:
        db.close()


@cli.command()
@click.option('--host', default='localhost', help='API host')
@click.option('--port', default=8000, help='API port')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def serve(host, port, reload):
    """Start the API server."""
    import uvicorn
    from market_scout.api import app
    
    click.echo(f"Starting API server at http://{host}:{port}")
    uvicorn.run(
        "market_scout.api:app",
        host=host,
        port=port,
        reload=reload
    )


if __name__ == '__main__':
    cli()