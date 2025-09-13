"""Database setup and utilities."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from market_scout.config import settings
from market_scout.models import Base


# Create database engine
engine = create_engine(settings.database_url, echo=settings.api_debug)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database."""
    create_tables()
