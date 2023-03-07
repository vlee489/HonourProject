"""API Routes"""
from .session import definition as session_definition
from .tournament import definition as tournament_definition

session_definitions = [
    session_definition,
    tournament_definition
]
