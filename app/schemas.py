"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    """Schema for creating a message"""
    message: str


class MessageResponse(BaseModel):
    """Schema for message response"""
    id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
