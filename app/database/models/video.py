from pydantic import BaseModel, Field
from .pydanticObjectID import PydanticObjectId
from typing import Optional

from .enums import Maps, Modes
from .tournament import Tournament


class Video(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: str
    tournament_id: PydanticObjectId
    tournament: Optional[Tournament]
    length: float  # In seconds & Milliseconds
    alpha_team: str
    bravo_team: str
    map: Maps
    mode: Modes
    url: str
