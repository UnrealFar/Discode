import asyncio
import aiohttp

class ClientUser:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        session: aiohttp.ClientSession,
        data: dict
    ):
        self.data: dict = data
        self.id: int = data.get("id")
        self.name: str = data.get("username")
        self.discriminator: int = data.get("discriminator")
        self.bio: str = data.get("bio")
        self.bot: bool = data.get("bot")
        self.email: str = data.get("email")
        self.__avatar: str = data.get("avatar")

    def __repr__(self):
        return f"<ClientUser id = {self.id} name = {self.name} discriminator = {self.discriminator}>"
    
    def __str__(self):
        return f"{self.name}#{self.discriminator}"
    
    @property
    def avatar_url(self):
        av = "https://cdn.discordapp.com/avatars/" + self.id + "/" + self.__avatar + ".png"
        return av
