"""Handled Tags"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from app.database.models import Tag, User, Video
from .exceptions import InvalidUserIDException, InvalidVideoIDException


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


async def add_video_tag(self: 'DBConnector', video_id: str, user_id: str, tags: dict, start: float, end: float,
                        description: str) -> Tag:
    """
    Add a tag to a video
    :param self:
    :param video_id:
    :param user_id:
    :param tags:
    :param start:
    :param end:
    :param description:
    :return:
    """
    if not (video := await self.get_id_video(video_id)):
        raise InvalidVideoIDException()
    if not (user := await self._db.Users.find_one({"_id": ObjectId(user_id)})):
        raise InvalidUserIDException()
    new_tag = {
        "user_id": user["_id"],
        "video_id": ObjectId(video.id),
        "start": start,
        "end": end,
        "description": description,
        "tags": tags
    }
    result_tag = await self._db.Tags.insert_one(new_tag)
    tag = Tag(**await self._db.Tags.find_one({"_id": result_tag.inserted_id}))
    tag.video = video
    tag.user = User(**user)
    return tag


async def delete_video_tag(self: 'DBConnector', tag_id: str) -> bool:
    """
    Delete a tag from a video
    :param self:
    :param tag_id:
    :return:
    """
    result = await self._db.Tags.delete_one({"_id": ObjectId(tag_id)})
    if result.deleted_count > 0:
        return True
    return False


