from pydantic import BaseModel, Field
from .pydanticObjectID import PydanticObjectId
from typing import Optional
from .user import User
from .video import Video


class Tag(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    user_id: PydanticObjectId
    user: Optional[User]
    video: Optional[Video]
    video_id: PydanticObjectId
    start: float
    end: float
    description: str
    tags: dict
