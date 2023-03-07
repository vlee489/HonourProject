from pydantic import BaseModel, Field
from .pydanticObjectID import PydanticObjectId


class User(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: str
    username: str
    password: str  # argon2 hash

