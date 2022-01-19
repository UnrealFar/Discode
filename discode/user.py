import asyncio
import aiohttp

__all__ = (
    "User",
    "ClientUser",
)

class User:
    __slots__ = [
        "id",
        "name",
        "discriminator",
        "bio",
        "bot",
        "system",
        "email",
        "_channel",
        "__avatar",
        "__banner",
        "http"
    ]

    r"""Represents a Discord user."""

    def __init__(self, **data):
        self.id = int(data.pop("id", int()))
        self.name = data.pop("username", None)
        self.discriminator: int = data.pop("discriminator", None)
        self.bio: str = data.pop("bio", None)
        self.bot: bool = data.pop("bot", False)
        self.system: bool = data.pop("system", False)
        self.email: str = data.pop("email", None)
        self.__avatar: str = data.pop("avatar", None)
        self.__banner: str = data.pop("banner", None)

        self.http = data.get("http")

    def __repr__(self):
        return f"<User: id={self.id} name={self.name} discriminator={self.discriminator}>"

    def __str__(self):
        return f"{self.name}#{self.discriminator}"

    @property
    def mention(self):
        """:class:`str`: Returns the user in a discord mention format i.e '@<{USER_ID}>.'"""
        return f"@<{self.id}>"

    @property
    def avatar_url(self):
        """:class:`str`: Returns the user's avatar url."""
        av = "https://cdn.discordapp.com/avatars/" + self.id + "/" + self.__avatar + ".png"
        return av

    @property
    def banner_url(self):
        """:class:`str`: Returns the user's banner url."""
        ba = "https://cdn.discord.com/banners/" + self.id + "/" + self.__banner + ".png"
        return ba

    @property
    def channel(self):
        return getattr(self, "_channel", None)

class ClientUser(User):
    r"""Represents the :class:`User` that is connected to Discord.
    """
    def __repr__(self) -> str:
        return f"<ClientUser id = {self.id} name = {self.name} discriminator = {self.discriminator}>"
