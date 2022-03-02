from typing import Any, Dict

from ..flags import UserFlags
from .assets import Asset
from .channel import DMChannel, Messageable

__all__ = (
    "User",
    "ClientUser"
    )


class User(Messageable):
    r"""Represents a Discord User."""

    __slots__ = (
        "id",
        "name",
        "discriminator",
        "bot",
        "system",
        "flags",
        "user_flags",
        "accent_colour",
        "dm_channel",
        "_avatar",
        "_banner",
        "_connection",
    )

    def __init__(self, connection, payload: Dict[str, Any]):
        self._connection = connection
        self.id = int(payload.pop("id"))
        self.name: str = payload.pop("username")
        self.discriminator: str = payload.pop("discriminator")
        self.bot: bool = payload.pop("bot", False)
        self._avatar: str = payload.pop("avatar", None)
        self._banner: str = payload.pop("banner", None)
        self.accent_colour = payload.pop("accent_color", 0)
        self.flags: UserFlags = UserFlags(payload.pop("flags", 0))
        self.public_flags: UserFlags = UserFlags(payload.pop("public_flags", 0))
        self.dm_channel: DMChannel = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id = {self.id} name = {self.name} discriminator = {self.discriminator} bot = {self.bot}>"

    def __str__(self) -> str:
        return f"{self.name}#{self.discriminator}"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def avatar(self) -> Asset:
        if self._avatar:
            return Asset.user_avatar(self)

    @property
    def banner(self) -> Asset:
        if self._banner:
            return Asset.user_banner(self)

    async def create_dm(self) -> DMChannel:
        http = self._connection.http
        p = await http.request(
            "POST", "/users/@me/channels", json={"recipient_id": str(self.id)}
        )
        p["user"] = self
        dm = DMChannel(self._connection, p)
        self.dm_channel = dm
        return dm


class ClientUser(User):
    r"""Represents the User that is connected to the gateway."""
