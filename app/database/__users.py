"""Handled User profiles"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .__init__ import DBConnector

from app.database.models import User


async def get_username_user(self: 'DBConnector', username: str) -> Optional[User]:
    """
    Get a user from
    :param self:
    :param username: User's username
    :return: User
    """
    result = await self._db.Users.find_one({"username": username})
    if result:
        return User(**result)
    return



