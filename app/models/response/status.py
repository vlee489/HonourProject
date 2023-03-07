"""Status response model"""
from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    status: bool = Field(description="Status of the request")
