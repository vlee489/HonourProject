from pydantic import BaseModel, Field
from typing import Dict, Union
from .user import User
from .video import Video


class Tag(BaseModel):
    _id: str = Field(description="The id of the tag")
    user: User = Field(description="The user that created the tag")
    video: Video = Field(description="The video that the tag is on")
    start: float = Field(description="The start time of the tag")
    end: float = Field(description="The end time of the tag")
    description: str = Field(description="The description of the tag")
    tags: Dict[str, Union[str, int, dict]] = Field(description="The tags of the tag")

