from pydantic import BaseModel, Field

from app.database.models.enums import Maps, Modes
from .tournament import Tournament


class Video(BaseModel):
    _id: str = Field(description="The id of the video")
    name: str = Field(description="The name of the video")
    tournament: Tournament = Field(description="The tournament the video is from")
    length: float = Field(description="Length of video in seconds and Milliseconds")
    alpha_team: str = Field(description="The name of the alpha team")
    bravo_team: str = Field(description="The name of the bravo team")
    map: Maps = Field(description="The game map the game is on")
    mode: Modes = Field(description="The game mode the game is on")
    url: str = Field(description="The url of the video")

