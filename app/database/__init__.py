import motor.motor_asyncio
from .exceptions import *


class DBConnector:
    def __init__(self, mongo_uri: str, db_name: str):
        """
        Constructor
        :param mongo_uri: MongoDB Connection URI
        :param db_name: DB Name
        """
        self._mongo_uri = mongo_uri
        self._db_name = db_name
        self._mongo_client: motor.motor_asyncio.AsyncIOMotorClient = None
        self._db: motor.motor_asyncio.AsyncIOMotorDatabase = None

    async def connect_db(self):
        """Create database connection."""
        self._mongo_client = motor.motor_asyncio.AsyncIOMotorClient(self._mongo_uri)
        self._db = self._mongo_client[self._db_name]

    async def close_mongo_connection(self):
        """Close database connection."""
        self._mongo_client.close()

    from app.database.__users import get_username_user
    from app.database.__videos import get_id_video, get_tournament_videos, add_video
    from app.database.__tournaments import get_id_tournament, get_all_tournaments, add_tournament
    from app.database.__tags import get_video_tags, add_video_tag, delete_video_tag
