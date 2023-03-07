from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

from .enums import Maps, Modes
from .tournament import Tournament


class Video(BaseModel):
    _id: ObjectId
    name: str
    tournament_id: ObjectId
    tournament: Optional[Tournament]
    length: float  # In seconds & Milliseconds
    alpha_team: str
    bravo_team: str
    map: Maps
    mode: Modes
    url: str

    class Config:
        json_encoders = {ObjectId: str}
