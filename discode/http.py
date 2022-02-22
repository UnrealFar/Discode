import asyncio
import json
from typing import Any, List, Dict, Optional

import aiohttp

from .connection import Connection
from .models import ClientUser, Message, Member


class HTTP:
    BASE_URL = "https://discord.com/api/v9"

    def __init__(
        self,
        client,
    ):
        self.client = client

    @property
    def connection(self) -> Connection:
        return self.client._connection

    async def request(self, method: str, url: str, **kwargs) -> Any:
        url = f"{self.BASE_URL}{url}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bot {self.client.token}"
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(kwargs.pop("json"))
        if "reason" in kwargs:
            headers["X-Audit-Log-Reason"] = kwargs.pop("X-Audit-Log-Reason")
        kwargs["headers"] = headers
        async with self._session.request(method, url, **kwargs) as req:
            if 300 > req.status >= 200:
                return await req.json()

    async def login(self):
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()
        p = await self.request("GET", "/users/@me")
        user = ClientUser(self.connection, p)
        self.connection.my_id = user.id
        return user

    async def logout(self):
        await self.request("POST", "/oauth/logout")

    async def close(self):
        if self._session:
            await self._session.close()

    async def send_message(
        self,
        channel_id: int,
        content: str = ...,
        *,
        embeds: List = ...
    ) -> Message:
        kwargs = {}
        
        if content != ...:
            kwargs["content"] = str(content)

        payload = await self.request(
            "POST",
            f"/channels/{channel_id}/messages",
            json = kwargs
        )

        return Message(self.connection, payload)

    async def edit_member(
        self,
        member: Member,
        payload: Dict[str, Any],
        reason: Optional[str] = ...,
    ):
        kwargs = {}
        kwargs["json"] = payload
        if reason != ...:
            kwargs["reason"] = reason
        await self.request(
            "PATCH",
            f"/guilds/{member.guild.id}/members/{member.id}",
            **kwargs
            )
