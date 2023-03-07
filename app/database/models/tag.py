from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from .user import User
from .video import Video


class Tag(BaseModel):
    _id: ObjectId
    user_id: ObjectId
    user: Optional[User]
    video: Optional[Video]
    video_id: ObjectId
    start: float
    end: float
    description: str
    tags: dict

    class Config:
        json_encoders = {ObjectId: str}
