import asyncio
from typing import Optional
import aiohttp

from .user import ClientUser

__all__ = (
    "HTTP",
)

class HTTP:
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_event_loop()
    ):
        self.loop: asyncio.AbstractEventLoop = loop
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(loop = self.loop)
        self.api_url = "https://discord.com/api/v9"

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict = {}
        ):
            headers: dict = {"Authorization": "Bot " + self.token}
            
            async with self.session.request(
                method = method,
                url = self.api_url + endpoint,
                params = params,
                headers = headers
            ) as resp:
                response = await resp.json()

                return response

    async def login(self, token: str):
        self.token = token
        try:
            data = await self.request("GET", "/users/@me")
        except:
            raise

        user = ClientUser(
            loop = self.loop,
            session = self.session,
            data = data
        )

        return user

    async def close(self):
        if not self.session.closed:
            await self.session.close()

    async def get_user(self, user_id: int):
        await self.request
