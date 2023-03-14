from pydantic import BaseModel, Field
from datetime import datetime


class SessionResponse(BaseModel):
    """Session response model"""
    session: str = Field(description="Session ID")
    expiry_date: datetime = Field(description="Session expiration time")
    delta: int = Field(description="Session expiration time in seconds")
