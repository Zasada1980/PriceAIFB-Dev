"""API endpoints for Market Scout Israel."""

from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from market_scout.models import Listing, ListingResponse, ProductCategory, ProductCondition
from market_scout.utils.database import get_db, init_db
from market_scout.config import settings


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for FastAPI app."""
    init_db()
    yield

app = FastAPI(
    title="Market Scout Israel API",
    description="Price monitoring system for computer components in Israeli secondary market",
    version="0.1.0",
    lifespan=lifespan
)
@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "Market Scout Israel API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/listings", response_model=List[ListingResponse])
async def get_listings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[ProductCategory] = None,
    condition: Optional[ProductCondition] = None,
    city: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    source_platform: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get listings with optional filtering."""
    query = db.query(Listing)
    
    # Apply filters
    if category:
        query = query.filter(Listing.category == category)
    if condition:
        query = query.filter(Listing.condition == condition)
    if city:
        query = query.filter(Listing.city.ilike(f"%{city}%"))
    if min_price:
        query = query.filter(Listing.price >= min_price)
    if max_price:
        query = query.filter(Listing.price <= max_price)
    if source_platform:
        query = query.filter(Listing.source_platform == source_platform)
    
    # Order by most recent
    query = query.order_by(desc(Listing.scraped_date))
    
    # Apply pagination
    listings = query.offset(skip).limit(limit).all()
    
    return listings


@app.get("/listings/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """Get a specific listing by ID."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@app.get("/stats/categories")
async def get_category_stats(db: Session = Depends(get_db)):
    """Get statistics by category."""
    stats = db.query(
        Listing.category,
        func.count(Listing.id).label('count'),
        func.avg(Listing.price).label('avg_price'),
        func.min(Listing.price).label('min_price'),
        func.max(Listing.price).label('max_price')
    ).group_by(Listing.category).all()
    
    return [
        {
            "category": stat.category,
            "count": stat.count,
            "avg_price": round(stat.avg_price, 2) if stat.avg_price else 0,
            "min_price": stat.min_price,
            "max_price": stat.max_price
        }
        for stat in stats
    ]


@app.get("/stats/cities")
async def get_city_stats(db: Session = Depends(get_db)):
    """Get statistics by city."""
    stats = db.query(
        Listing.city,
        func.count(Listing.id).label('count'),
        func.avg(Listing.price).label('avg_price')
    ).filter(Listing.city.isnot(None)).group_by(Listing.city).order_by(desc('count')).limit(20).all()
    
    return [
        {
            "city": stat.city,
            "count": stat.count,
            "avg_price": round(stat.avg_price, 2) if stat.avg_price else 0
        }
        for stat in stats
    ]


@app.get("/stats/trends")
async def get_price_trends(
    category: Optional[ProductCategory] = None,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get price trends over time."""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(
        func.date(Listing.scraped_date).label('date'),
        func.count(Listing.id).label('count'),
        func.avg(Listing.price).label('avg_price')
    ).filter(Listing.scraped_date >= start_date)
    
    if category:
        query = query.filter(Listing.category == category)
    
    trends = query.group_by(func.date(Listing.scraped_date)).order_by('date').all()
    
    return [
        {
            "date": trend.date.isoformat(),
            "count": trend.count,
            "avg_price": round(trend.avg_price, 2) if trend.avg_price else 0
        }
        for trend in trends
    ]


@app.get("/search")
async def search_listings(
    q: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Search listings by text."""
    query = db.query(Listing).filter(
        (Listing.title.ilike(f"%{q}%")) |
        (Listing.description.ilike(f"%{q}%")) |
        (Listing.brand.ilike(f"%{q}%")) |
        (Listing.model.ilike(f"%{q}%"))
    )
    
    # Order by relevance (most recent first for now)
    query = query.order_by(desc(Listing.scraped_date))
    
    # Apply pagination
    listings = query.offset(skip).limit(limit).all()
    
    return [ListingResponse.from_orm(listing) for listing in listings]