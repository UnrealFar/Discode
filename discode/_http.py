import asyncio
from typing import Optional
import aiohttp

from .user import ClientUser
from . import gw

__all__ = ("HTTP",)


class HTTP:
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_event_loop(),
        **kwargs
    ):
        self.loop: asyncio.AbstractEventLoop = loop
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(loop=self.loop)
        self.client: ClientUser = kwargs.get("client")
        self.api_url = "https://discord.com/api/v9"
        self.intents = kwargs.get("intents", 0)
        self.user_agent = "DiscordBot made with Discode"

    async def request(self, method: str, endpoint: str, params: dict = {}):
        headers: dict = {"Authorization": "Bot " + self.token}

        async with self.session.request(
            method=method, url=self.api_url + endpoint, params=params, headers=headers
        ) as resp:
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
            "dispatch": self.client.dispatch
        }
        self.ws = gw.WS(data)
        await self.ws.handle()

    async def login(self, token: str):
        self.token = token
        try:
            data = await self.request("GET", "/users/@me")
        except Exception as e:
            raise e

        data["http"] = self
        self.user = ClientUser(loop=self.loop, data=data)

        return self.user

    async def close(self):
        if not self.session.closed:
            await self.session.close()

    async def get_user(self, user_id: int):
        await self.request()
