import asyncio
from typing import Union

from .user import User
from .channel import TextChannel, Channel
from .guild import Guild

__all__ = ("Message",)


class Message:
    r"""Represents a Discord message."""

    def __init__(self, loop: asyncio.AbstractEventLoop, data: dict):
        self.data = data
        self.loop = loop
        self.http = data.get("http")
        self.id: int = data.get("id")
        self.content: str = data.get("content")
        self.created_at = data.get("timestamp")
        self.mentions = data.get("mentions")
        self.__author: dict = data.get("author")
        self.__member: dict = data.get("member")
        self.edited_at = data.get("edited_timestamp")

    @property
    def author(self) -> User:
        """Returns a member object if in a guild, else a user object."""
        data = self.__author
        data["http"] = self.http
        return User(loop=self.loop, data=data)

    @property
    def guild(self) -> Guild:
        """Returns the :class:`Guild` to which the message belongs to.
        """
        return self.http.client.get_guild(self.guild_id)

    @property
    def channel(self) -> Union[Channel, TextChannel]:
        return self.http.client.get_channel(self.channel_id, self.guild_id)

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
