from pydantic import BaseModel, Field
from app.database.models import Maps, Modes


class AddVideo(BaseModel):
    name: str = Field(description="Name of the video")
    length: float = Field(description="Length of the video in seconds")
    alpha_team: str = Field(description="Name of the alpha team")
    bravo_team: str = Field(description="Name of the bravo team")
    map: Maps = Field(description="Map of the video")
    mode: Modes = Field(description="Mode of the video")
    url: str = Field(description="URL of the video")
