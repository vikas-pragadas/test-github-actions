"""Database models"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Message(Base):
    """Example model for storing messages"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Message(id={self.id}, message='{self.message}')>"
