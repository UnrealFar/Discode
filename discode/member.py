from typing import Optional, Any

from .user import User
from .channel import DMChannel

class Member:
    __slots__ = (
        "user",
        "id",
        "name",
        "discriminator",
        "nick",
        "bot",
        "joined_at",
        "channel",
        "http"
    )

    r"""Represents a Discord guild member.
    """
    def __init__(self, **data):
        self.http = data.get("http")
        self.user: User = User(**data.get("user"))
        self.id = int(self.user.id)
        self.name = self.user.name
        self.discriminator = self.user.discriminator
        self.nick = data.pop("nick", None)
        self.bot: bool = self.user.bot
        self.joined_at = data.pop("joined_at", None)

    def __str__(self) -> str:
        return f"{self.name}#{self.discriminator}"

    def __eq__(self, other: Any) -> bool:
        return (self == other) or (self.id == getattr(other, "id"))

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"

    @property
    def display_name(self) -> str:
        if not self.nick:
            return self.name
        return self.nick

    @property
    def roles(self):
        return self.data.get("roles")

    async def send(self, *content: Optional[str], **kwargs):

        ch = await self._get_channel()

        return await ch.send(
            *content,
            **kwargs
        )

    async def _get_channel(self):
        if not hasattr(self.user, "_channel"):
            json = {"recipient_id": self.id}
            req = await self.http.request(
                "POST",
                "/users/@me/channels",
                json = json
            )
            data = {}
            data["channel_id"] = req.pop("id", None)
            data["http"] = self
            self.user._channel = DMChannel(**data)
        return self.user.channel
