"""Database configuration and connection"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import os

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Only create engine if DATABASE_URL is provided
if DATABASE_URL:
    # Create SQLAlchemy engine
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,
        max_overflow=10
    )
    
    # Create SessionLocal class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Database dependency for FastAPI routes
    Yields a database session and closes it after use
    """
    if not SessionLocal:
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Please set DATABASE_URL environment variable."
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables
    Call this on application startup
    """
    if not DATABASE_URL:
        print("⚠️ DATABASE_URL not set. Database features will be disabled.")
        return
    
    if not engine:
        print("⚠️ Database engine not initialized.")
        return
        
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not create database tables: {e}")
