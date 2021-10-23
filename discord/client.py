import aiohttp
import asyncio
import signal

from .http_client import HTTPClient

class Client:
    def __init__(
        self
    ):
        self.token: str = ""
        self.http = HTTPClient(self.token)

    def run(self, token: str):
        self.token = token.strip()
        asyncio.run(self.http.static_login(self.token))