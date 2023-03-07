"""Handled Videos"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId

from app.database.models import Video


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
