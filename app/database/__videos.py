"""Handled Videos"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId

from app.database.models import Video, Maps, Modes
from .exceptions import InvalidTournamentIDException


async def get_id_video(self: 'DBConnector', video_id: str) -> Optional[Video]:
    """
    Get video from ID
    :param self:
    :param video_id: Video ID
    :return: Video or None
    """
    result = await self._db.Videos.find_one({"_id": ObjectId(video_id)})
    if result:
        tour = await self.get_id_tournament(result["tournament_id"])
        video = Video(**result)
        video.tournament = tour
        return video
    return


async def get_tournament_videos(self: 'DBConnector', tour_id: str) -> List[Video]:
    """
    Get all videos from a tournament
    :param self:
    :param tour_id: Tournament ID
    :return: List of Videos
    """
    videos = []
    if tour := await self.get_id_tournament(tour_id):
        async for video in self._db.Videos.find({"tournament_id": ObjectId(tour_id)}):
            video = Video(**video)
            video.tournament = tour
            videos.append(video)
    return videos


async def add_video(self: 'DBConnector', tournament_id: str, name: str, length: float, alpha_team: str, bravo_team: str,
                    map: Maps, mode: Modes, url: str) -> Video:
    """
    Add a video
    :param self:
    :param tournament_id:
    :param name:
    :param length:
    :param alpha_team:
    :param bravo_team:
    :param map:
    :param mode:
    :param url:
    :return:
    """
    if not (await self.get_id_tournament(tournament_id)):
        raise InvalidTournamentIDException
    result = await self._db.Videos.insert_one({
        "name": name,
        "tournament_id": ObjectId(tournament_id),
        "length": length,
        "alpha_team": alpha_team,
        "bravo_team": bravo_team,
        "map": map,
        "mode": mode,
        "url": url,
    })
    return await self.get_id_video(str(result.inserted_id))

