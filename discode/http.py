import asyncio
import json
from typing import Any, Dict, Optional

import aiohttp

from .connection import Connection
from .gateway import Gateway
from .models import ClientUser


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

    async def edit_member(
        self,
        guild_id: int,
        member_id: int,
        payload: Dict[str, Any],
        reason: Optional[str] = ...,
    ):
        kwargs = dict()
        kwargs["json"] = payload
        if reason != ...:
            kwargs["reason"] = reason
        await self.request("PATCH", f"/guilds/{guild_id}/members/{member_id}", **kwargs)
