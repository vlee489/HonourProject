from pydantic import BaseModel
from bson import ObjectId


class User(BaseModel):
    _id: ObjectId
    name: str
    username: str
    password: str  # argon2 hash

    @property
    def id(self) -> str:
        return str(self._id)

    class Config:
        json_encoders = {ObjectId: str}

