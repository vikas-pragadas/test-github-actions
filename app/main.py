"""FastAPI application with database connection"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db, init_db
from app import models, schemas
import os

app = FastAPI(
    title="FastAPI with PostgreSQL",
    description="FastAPI application connected to AWS RDS PostgreSQL",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")


@app.get("/")
def home():
    """Root endpoint"""
    return {
        "message": "Welcome to the API",
        "database": "Connected to PostgreSQL"
    }


@app.get("/hello")
def read_hello():
    """Hello endpoint"""
    return {"message": "Hello World"}


@app.get("/apprunner")
def apprunner():
    """App Runner test endpoint"""
    return {"message": "AWS is configured and App Runner successfully"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint - tests database connection"""
    try:
        # Try to query database
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


@app.post("/messages", response_model=schemas.MessageResponse)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    """Create a new message in the database"""
    try:
        db_message = models.Message(message=message.message)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create message: {str(e)}")


@app.get("/messages", response_model=list[schemas.MessageResponse])
def get_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all messages from the database"""
    try:
        messages = db.query(models.Message).offset(skip).limit(limit).all()
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch messages: {str(e)}")


@app.get("/messages/{message_id}", response_model=schemas.MessageResponse)
def get_message(message_id: int, db: Session = Depends(get_db)):
    """Get a specific message by ID"""
    try:
        message = db.query(models.Message).filter(models.Message.id == message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return message
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch message: {str(e)}")