import asyncio
from typing import Optional, Union
import aiohttp

from .user import ClientUser
from .intents import Intents
from .message import Message
from .channel import TextChannel
from . import gw

__all__ = ("HTTP",)


class HTTP:
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_event_loop(), **kwargs):
        self.loop: asyncio.AbstractEventLoop = loop
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.client: ClientUser = kwargs.get("client")
        self.api_url = "https://discord.com/api/v9"
        self.intents: Intents = kwargs.get("intents")
        self.user_agent = "DiscordBot made with Discode"

    async def request(self, method: str, endpoint: str, **kwargs):
        headers = {"Authorization": "Bot " + self.token}

        async with self.session.request(method=method, url=self.api_url + endpoint, headers=headers, **kwargs) as resp:
            response = await resp.json()

            return response

    async def connect(self):
        if self.session.closed:
            self.session = aiohttp.ClientSession()

        data = {
            "loop": self.loop,
            "token": self.token,
            "intents": self.intents,
            "http": self,
            "dispatch": self.client.dispatch,
        }
        self.ws = gw.WS(data)
        await self.ws.handle()

    async def login(self, token: str):
        self.token = token
        try:
            data = await self.request("GET", "/users/@me")
        except:
            raise

        data["http"] = self
        self.user = ClientUser(loop=self.loop, data=data)

        return self.user

    async def close(self):
        if not self.session.closed:
            await self.session.close()

    async def send_message(self, channel_id, **kwargs) -> Message:
        data = {}

        if kwargs.get("content", None):
            data["content"] = str(kwargs.pop("content"))

        if kwargs.get("embed", None):
            data["embeds"] = [kwargs.pop("embed").data]

        if kwargs.get("embeds", None):
            if "embeds" not in data:
                data["embeds"] = []
            embeds = kwargs.pop("embeds")
            for embed in embeds:
                data["embeds"].append(embed.data)

        print(data)
        msgdata = await self.request("POST", f"/channels/{channel_id}/messages", json=data)
        msgdata["http"] = self
        print(msgdata)
        return Message(loop=self.loop, data=msgdata)

    async def fetch_channel(self, channel_id: int) -> Union[TextChannel]:
        data = await self.request("GET", f"/channels/{channel_id}")
        data["http"] = self
        return TextChannel(loop=self.loop, data=data)
