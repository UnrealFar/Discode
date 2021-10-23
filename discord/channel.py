import aiohttp
import asyncio
import os

from .client import Client
from .message import Message
from .embed import Embed

base_url = "https://discord.com/api/v9"

class Channel:  
    def __init__(
        self,
        channel_id: int,
    ):
        self.channel_id = channel_id
        self.client = Client()
        self.http = self.client.http

    async def send(self, message: str, embed: Embed = None):
        tosend = {}
        tosend["content"] = message

        if embed is not None:
            try:
                emb = embed.get_embed
                tosend["embeds"].append(emb)
            except:
                emb = embed.get_embed
                tosend["embeds"] = [emb]

        await self.http.request("POST", f"/channels/{self.channel_id}/messages", json = tosend)