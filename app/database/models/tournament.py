from pydantic import BaseModel, Field
from datetime import datetime
from .pydanticObjectID import PydanticObjectId


class Tournament(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: str
    date: datetime
    organizer: str
