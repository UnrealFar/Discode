import aiohttp
import asyncio
import signal

from .http import HTTPClient

base_url = "https://discord.com/api/v9"

class Client:
    def __init__(
        self,
        token: str,
    ):
        self.token = token.strip()
        self.http = HTTPClient(self.token)

    @property
    def get_token(self):
        return self.token

    async def login(self):
        await self.http.static_login(token = self.token)

    async def start(self):
        await self.login()