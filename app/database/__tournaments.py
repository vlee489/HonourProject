"""Handled Tournaments"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId

from app.database.models import Tournament


async def get_all_tournaments(self: 'DBConnector') -> List[Tournament]:
    """
    Get all tournaments
    :param self:
    :return: List of Tournaments
    """
    tournaments = []
    async for tour in self._db.Tournaments.find():
        tournaments.append(Tournament(**tour))
    return tournaments


async def get_id_tournament(self: 'DBConnector', tour_id: str) -> Optional[Tournament]:
    """
    Get tournament from ID
    :param self:
    :param tour_id: Tournament ID
    :return: Tournament or None
    """
    result = await self._db.Tournaments.find_one({"_id": ObjectId(tour_id)})
    if result:
        return Tournament(**result)
    return
