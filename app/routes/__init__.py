"""API Routes"""
from .session import definition as session_definition
from .tournament import definition as tournament_definition
from .videos import definition as video_definition
from .tags import definition as tag_definition

session_definitions = [
    session_definition,
    tournament_definition,
    video_definition,
    tag_definition
]
