from typing import Any, Dict, Union

from .abc import Snowflake
from .channel import TextChannel
from .guild import Guild
from .member import Member
from .user import User

__all__ = ("Message",)


class Message(Snowflake):

    __slots__ = ("id", "content", "channel_id", "guild_id", "author_id", "_connection")

    def __init__(self, connection, payload: Dict[str, Any]):
        self._connection = connection
        self.id: int = int(payload.pop("id"))
        self.content: str = payload.pop("content", None)
        self.channel_id: int = int(payload.pop("channel_id"))
        g_id = payload.pop("guild_id", None)
        self.guild_id: int = int(g_id) if g_id else None
        self.author_id: int = int(payload.pop("author").get("id", 0))
        del payload

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id = {self.id} content = {self.content}"

    def __str__(self) -> str:
        return self.content or ""

    @property
    def author(self) -> Union[User, Member]:
        g = self.guild
        if g:
            return g.get_member(self.author_id)
        return self._connection.get_user(self.author_id)

    @property
    def channel(self) -> TextChannel:
        return self._connection.channel_cache.get(self.channel_id)

    @property
    def guild(self) -> Guild:
        return self._connection.get_guild(self.guild_id)
