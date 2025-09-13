"""Database models for Market Scout Israel."""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel


Base = declarative_base()


class ProductCondition(str, Enum):
    """Product condition enumeration."""
    NEW = "new"
    LIKE_NEW = "like_new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    FOR_PARTS = "for_parts"


class ProductCategory(str, Enum):
    """Product category enumeration."""
    CPU = "cpu"
    GPU = "gpu"
    MOTHERBOARD = "motherboard"
    RAM = "ram"
    STORAGE = "storage"
    PSU = "psu"
    COOLING = "cooling"
    CASE = "case"
    COMPLETE_BUILD = "complete_build"
    OTHER = "other"


class Listing(Base):
    """Database model for product listings."""
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False, index=True)
    currency = Column(String(3), default="ILS")
    
    # Product information
    category = Column(SQLEnum(ProductCategory), nullable=False, index=True)
    condition = Column(SQLEnum(ProductCondition), nullable=False, index=True)
    brand = Column(String(100), index=True)
    model = Column(String(200), index=True)
    
    # Location information
    city = Column(String(100), index=True)
    region = Column(String(100), index=True)
    
    # Seller information
    seller_name = Column(String(200))
    seller_contact = Column(String(200))
    
    # Source information
    source_platform = Column(String(50), nullable=False, index=True)
    source_url = Column(String(1000))
    source_id = Column(String(200), index=True)
    
    # Warranty and additional info
    warranty_months = Column(Integer)
    has_original_box = Column(String(10))  # yes/no/unknown
    has_receipt = Column(String(10))  # yes/no/unknown
    
    # Timestamps
    posted_date = Column(DateTime)
    scraped_date = Column(DateTime, default=datetime.utcnow, index=True)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = Column(String(10), default="yes", index=True)  # yes/no/unknown


# Pydantic models for API
class ListingBase(BaseModel):
    """Base Pydantic model for listings."""
    title: str
    description: Optional[str] = None
    price: float
    currency: str = "ILS"
    category: ProductCategory
    condition: ProductCondition
    brand: Optional[str] = None
    model: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    seller_name: Optional[str] = None
    source_platform: str
    source_url: Optional[str] = None
    source_id: Optional[str] = None
    warranty_months: Optional[int] = None
    has_original_box: Optional[str] = None
    has_receipt: Optional[str] = None
    posted_date: Optional[datetime] = None


class ListingCreate(ListingBase):
    """Pydantic model for creating listings."""
    pass


class ListingResponse(ListingBase):
    """Pydantic model for listing responses."""
    id: int
    scraped_date: datetime
    updated_date: datetime
    is_active: str

    class Config:
        from_attributes = True
        model_config = {"from_attributes": True}