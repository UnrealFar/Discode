import asyncio
from typing import Optional

__all__ = ("TextChannel", "DMChannel")


class Channel:
    r"""Represents the base for a Discord channel.
    This can be a :class:`TextChannel`, a Category, a VoiceChannel, or a Thread.
    """

    def __init__(self, **data):
        self.data: dict = data
        self.http = data.get("http")
        self.id = int(data.pop("id", None))
        self.name = data.pop("name", None)
        self.topic = data.get("topic")
        self.permissions = data.get("permission_overwrites")
        self.position = data.get("position")

    @property
    def mention(self) -> str:
        return f"<#{self.id}>"

    @property
    def is_nsfw(self) -> bool:
        return self.data.get("nsfw", False)

class TextChannel(Channel):
    r"""Represents a Discord text channel.
    A text channel is a normal channel inside of a guild in which users can chat.
    """
    __slots__ = (
        "id",
        "guild_id",
        "type",
        "_guild",
        "http"
    )

    def __init__(
        self,
        id,
        *,
        guild = None,
        http = None,
        **kwargs
    ):
        del kwargs
        self.id: int = int(id)
        self.type: int = 0
        self._guild = guild
        self.http = http

    @property
    def guild(self):
        r"""Get the guild that the text channel belongs to.
        """
        return self._guild

    async def send(
        self,
        *content: Optional[str],
        **kwargs
    ):
        r"""Send a message to the text channel. Returns the sent :class:`Message`.
        """
        print(self.id)
        return await self.http.send_message(
            self.id,
            *content,
            **kwargs,
        )

    def copy(self):
        return TextChannel(
            id = self.id,
        )

class DMChannel(Channel):
    __slots__ = (
        "id",
        "type",
        "user",
        "http"
    )

    def __init__(
        self,
        channel_id,
        *,
        user = None,
        http = None
    ):
        self.id: int = int(channel_id)
        self.type: int = 1
        self.user = None
        self.http = http

    async def send(
        self,
        *content: Optional[str],
        **kwargs
    ):

        return await self.http.send_message(
            self.id,
            *content,
            **kwargs
        )
