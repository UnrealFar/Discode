import aiohttp
import asyncio
import os

from .http import Route

base_url = Route().BASE

class Channel:

    async def send(token:str, channel_id: int, message: str):
        msg = {"content": f"{message}"}
        headers = {"Authorization": f"Bot {token}"}
        async with aiohttp.ClientSession(headers = headers) as ses:
            async with ses.post(url = f"{base_url}/channels/{channel_id}/messages", json = msg):
                pass

    async def get_channel(token:str, channel_id: int):
        headers = {"Authorization": f"Bot {token}"}
        async with aiohttp.ClientSession(headers = headers) as ses:
            async with ses.get(f"{base_url}/channels/{channel_id}") as ch:
                channel = await ch.json()
                return print(channel)