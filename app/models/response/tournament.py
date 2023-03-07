from pydantic import BaseModel, Field
from datetime import datetime


class Tournament(BaseModel):
    _
    id: str = Field(description="The id of the tournament")
    name: str = Field(description="The name of the tournament")
    date: datetime = Field(description="The start date & time of the tournament")
    organizer: str = Field(description="The name of the organizer of the tournament")
