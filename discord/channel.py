import aiohttp
import asyncio
import os

from .http import Route, HTTPClient
from .client import Client
from .message import Message
from .embed import Embed

base_url = "https://discord.com/api/v9"

class Channel:  
    def __init__(
        self,
        channel_id: int,
        token: str
    ):
        self.channel_id = channel_id
        self.token = token
        self.http = HTTPClient

    async def send(self, message: str, embed: Embed = None):
        tosend = {}
        tosend["content"] = message
        if embed is not None:
            try:
                tosend["embeds"].append(embed.embed)
            except:
                tosend["embeds"] = [embed.embed]

        await self.http(token = str(self.token)).request(Route("POST", f"/channels/{self.channel_id}/messages"), j = tosend)