from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class Tournament(BaseModel):
    _id: ObjectId
    name: str
    date: datetime
    organizer: str

    class Config:
        json_encoders = {ObjectId: str}
