"""Handled Tags"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from app.database.models import Tag, User, Video


async def get_video_tags(self: 'DBConnector', video_id: str) -> List[Tag]:
    """
    Get list of tags for a Video
    :param self:
    :param video_id:
    :return:
    """
    tags = []
    async for tag in self._db.Tags.aggregate([
        {
            u"$match": {
                u"video_id": ObjectId(video_id)
            }
        },
        {
            u"$lookup": {
                u"from": u"Videos",
                u"localField": u"video_id",
                u"foreignField": u"_id",
                u"as": u"video"
            }
        },
        {
            u"$lookup": {
                u"from": u"Users",
                u"localField": u"user_id",
                u"foreignField": u"_id",
                u"as": u"user"
            }
        },
        {
            u"$unwind": {
                u"path": u"$video"
            }
        },
        {
            u"$unwind": {
                u"path": u"$user"
            }
        },
    {
        u"$lookup": {
            u"from": u"Tournaments",
            u"localField": u"video.tournament_id",
            u"foreignField": u"_id",
            u"as": u"video.tournament"
        }
    },
    {
        u"$unwind": {
            u"path": u"$video.tournament"
        }
    }
    ]):
        tags.append(Tag(**tag))
    return tags
