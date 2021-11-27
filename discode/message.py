import asyncio

from .user import User

__all__ = ("Message",)

class Message:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        data: dict
    ):
        self.id: int = data.get("id")
        self.content: str = data.get("content", None)
        self.timestamp = data.get("timestamp")
        self.__guild_id = data.get("guild_id")
        self.__channel_id = data.get("channel_id")
        self.__author: dict = data.get("author")

        self.loop: asyncio.AbstractEventLoop = loop
        self.http = data.get("http")

    @property
    def author(self) -> User:
        data = self.__author
        data["http"] = self.http
        return User(
            loop = self.loop,
            data = data
        )
