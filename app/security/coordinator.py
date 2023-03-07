"""
Security Coordinator
Handles all security management & authentication
"""
from redis import asyncio as aioredis
import uuid
import msgpack
from fastapi import Request
import datetime
from typing import Optional
import argon2

from app.database import DBConnector
from app.functions.packer import pack, unpack
from .models.session import Session


class SecurityCoordinator:
    """API Security Coordinator"""

    def __init__(self, redis_uri: str, database: DBConnector):
        self.__redis_uri = redis_uri
        self.__redis_client: Optional[aioredis.client] = None
        self.__database = database
        self.__ph = argon2.PasswordHasher()

    async def start_up(self):
        """Start up functions."""
        self.__redis_client = await aioredis.from_url(self.__redis_uri)

    async def _cache_set_key(self, key: str, value: dict) -> bool:
        """
        Add Key:Value to Redis cache
        :param key: Key name
        :param value: Value Data dict
        :return: if operation was successful
        """
        _value = pack(value)
        async with self.__redis_client.client() as conn:
            return await conn.execute_command("SET", f"{key}", _value, "EX", "10800")

    async def _cache_get_key(self, key: str) -> Optional[dict]:
        """
        Retrieve value via key from Redis cache
        :param key: Key to retrieve data from
        :return: None or dict
        """
        if value := await self.__redis_client.get(f"{key}"):
            return unpack(value)

    async def _cache_delete_key(self, key: str) -> None:
        """
        delete value via key from Redis cache
        :param key: Key to delete
        :return: None
        """
        await self.__redis_client.delete(f"{key}")

    async def create_session(self, request: Request, username: str, password: str) -> bool:
        """
        Completes Authorization Code Grant Request and creates session
        :param request: User's request
        :param username: User's username
        :param password: User's password
        :return: if successful
        """
        await self.delete_session(request)  # delete existing sessions for user
        if not (user := await self.__database.get_username_user(username)):
            return False
        # Check if password is valid
        try:
            self.__ph.verify(user.password, password)
        except argon2.exceptions.VerifyMismatchError:
            return False
        # If user gets past checks
        session_id = uuid.uuid4().hex
        expiry_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=10800)
        session_data = Session(
            user_id=user.id,
            username=user.username,
            expiry_date=expiry_date
        )
        if await self._cache_set_key(session_id, session_data.dict()):
            request.session['security'] = {"session": session_id}
            return True

    async def delete_session(self, request: Request):
        """
        Delete a user's session (aka logout)
        :param request: User's request
        :return: None
        """
        if session_security := request.session.get("security"):
            if session_id := session_security.get("session", ""):
                await self._cache_delete_key(session_id)
                request.session.pop("security", {})
                return True
        return False

    async def get_session(self, request: Request) -> Optional[Session]:
        """
        Get a user's session
        :param request: User's request
        :return: Session or None
        """
        if session_security := request.session.get("security"):
            if session_id := session_security.get("session", ""):
                if session_data := await self._cache_get_key(session_id):
                    return Session(**session_data)
        return None

