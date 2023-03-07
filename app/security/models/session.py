from pydantic import BaseModel
from datetime import datetime


class Session(BaseModel):
    user_id: str
    username: str
    expires: datetime
