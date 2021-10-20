import aiohttp
import asyncio
import os

from .http import Route
from .client import Client
from .message import Message

base_url = "https://discord.com/api/v9"

class Channel:  
    def __init__(
        self,
        channel_id: int
    ):
        self.channel_id = channel_id
        self.token = "a"#token

    async def send(self, message: str):
        await Message(token = self.token, channel_id = self.channel_id, content = message).send_message()