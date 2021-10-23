import aiohttp
import asyncio
import signal

from .http_client import HTTPClient

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