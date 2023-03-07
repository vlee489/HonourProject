from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(description="The id of the user")
    name: str = Field(description="The name of the user")
    username: str = Field(description="The username of the user")
