import asyncio
from typing import Union

from .user import User
from .channel import TextChannel, Channel
from .member import Member
from .guild import Guild

__all__ = ("Message",)


class Message:
    r"""Represents a Discord message."""

    def __init__(self, **data):
        self.data = data
        self.http = data.get("http")
        self.loop = self.http.loop
        self.created_at = data.get("timestamp")
        self.mentions = data.get("mentions")
        self._content = data.get("content")
        self.__author: dict = data.get("author")
        self.__member: dict = data.get("member")
        self.edited_at = data.get("edited_timestamp")

    @property
    def id(self) -> int:
        return int(self.data.get("id"))

    @property
    def content(self) -> str:
        return self._content

    @property
    def author(self) -> User:
        """Returns a member object if in a guild, else a user object."""
        data = self.__author
        data["http"] = self.http
        if self.guild:
            data = self.__member
            data["http"] = self.http
            data["user"] = self.__author
            return Member(**data)
        return User(**data)

    @property
    def guild(self) -> Guild:
        """Returns the :class:`Guild` to which the message belongs to.
        """
        return self.http.client.get_guild(self.guild_id)

    @property
    def guild_id(self) -> int:
        try:
            return int(self.data.get("guild_id"))
        except: return None

    @property
    def channel_id(self) -> int:
        try:
            return int(self.data.get("channel_id"))
        except: return None
    
    @property
    def channel(self):
        return self.http.client.get_channel(self.channel_id, self.guild_id)

    def set_content(content: str):
        self._content = content

    @property
    def components(self):
        return self.data.get("components")

