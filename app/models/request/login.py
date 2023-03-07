"""Session Login request"""
from pydantic import BaseModel, Field


class LoginCredentials(BaseModel):
    username: str
    password: str = Field(min_length=8)
