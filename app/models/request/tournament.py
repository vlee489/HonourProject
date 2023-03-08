from pydantic import BaseModel, Field


class AddTournament(BaseModel):
    name: str = Field(description="Name of the tournament")
    date: str = Field(description="Date of the tournament")
    organizer: str = Field(description="Organizer of the tournament")
