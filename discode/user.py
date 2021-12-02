import asyncio
import aiohttp

__all__ = (
    "User",
    "ClientUser",
)

class User:
    r"""Represents a Discord user."""

    def __init__(self, **data):
        self.data: dict = data
        self.discriminator: int = data.get("discriminator")
        self.bio: str = data.get("bio")
        self.bot: bool = data.get("bot", False)
        self.system: bool = data.get("system", False)
        self.email: str = data.get("email")
        self.__avatar: str = data.get("avatar")
        self.__banner: str = data.get("banner", None)

        self.http = data.get("http")
        self.loop = self.http.loop

    def __repr__(self):
        return f"<User: id={self.id} name={self.name} discriminator={self.discriminator}>"

    def __str__(self):
        return f"{self.name}#{self.discriminator}"

    @property
    def id(self) -> int:
        return int(self.data.get("id"))

    @property
    def name(self) -> str:
        return self.data.get("username")

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


class ClientUser(User):
    r"""Represents the :class:`User` that is connected to Discord.
    """

    def __init__(self, **data):
        super().__init__(**data)

    def __repr__(self) -> str:
        return f"<ClientUser id = {self.id} name = {self.name} discriminator = {self.discriminator}>"
