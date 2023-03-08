from pydantic import BaseModel, Field
from typing import Dict, Union


class AddTag(BaseModel):
    start: float = Field(description="Start time of the tag", ge=0)
    end: float = Field(description="End time of the tag", gt=0)
    description: str = Field(description="Description of the tag")
    tags: Dict[str, Union[str, int, dict]] = Field(description="Tags for the tag")
