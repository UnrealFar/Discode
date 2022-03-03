import asyncio
import json
from typing import TYPE_CHECKING, Any, Dict, List, Sequence, Optional

import aiohttp

from .connection import Connection
from .models import ClientUser, Member, Message
from .dataclasses import Embed, File
from .utils import UNDEFINED

if TYPE_CHECKING:
    from .client import Client


class HTTP:
    BASE_URL = "https://discord.com/api/v10"

    def __init__(
        self,
        client,
    ):
        self.client: Client = client

    @property
    def connection(self) -> Connection:
        return self.client._connection

    async def request(
        self,
        method: str,
        url: str,
        form: Optional[List[Dict[str, Any]]] = UNDEFINED,
        **kwargs
    ) -> Any:
        url = f"{self.BASE_URL}{url}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bot {self.client.token}"
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(kwargs.pop("json"))
        elif form != UNDEFINED:
            form_data = aiohttp.FormData()
            for f in form:
                form_data.add_field(**f)
            kwargs["data"] = form_data
        if "reason" in kwargs:
            headers["X-Audit-Log-Reason"] = kwargs.pop("X-Audit-Log-Reason")
        kwargs["headers"] = headers
        async with self._session.request(method, url, **kwargs) as req:
            if 300 > req.status >= 200:
                return await req.json()
            else:
                try:
                    e = await req.json()
                except:
                    raise Exception(await req.text())
                raise Exception(e.get("message"))

    async def login(self):
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.BASE_URL = self.BASE_URL.replace("v10", f"v{self.client.api_version}")
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
        *,
        content: str = UNDEFINED,
        embed: Embed = UNDEFINED,
        file: File = UNDEFINED,
        embeds: List[Embed] = [],
        files: List[File] = [],
    ) -> Message:
        kwargs = {}

        if content != UNDEFINED:
            kwargs["content"] = str(content)

        if embed != UNDEFINED:
            kwargs["embeds"] = (embed.to_dict(),)

        if len(embeds) > 0:
            kwargs["embeds"] = kwargs.pop("embeds") if "embeds" in kwargs else list()
            for emb in embeds:
                kwargs["embeds"].append(emb.to_dict())

        if len(files) == 0 and file == UNDEFINED:
            payload = await self.request(
                "POST", f"/channels/{channel_id}/messages", json=kwargs
            )

        else:
            form = []
            form.append({"name": "payload_json", "value": json.dumps(kwargs)})
            if file:
                files.append(file)
            if len(files) == 1:
                file = files[0]
                form.append(
                    {
                        "name": f"file",
                        "value": file.fp,
                        "filename": file.filename,
                        "content_type": "application/octet-stream"
                    }
                )
            elif len(files) > 1:
                for i, f in enumerate(files):
                    form.append(
                        {
                            "name": f"file{i}",
                            "value": f.fp,
                            "filename": f.filename,
                            "content_type": "application/octet-stream",
                        }
                    )
            payload = await self.request(
                "POST",
                f"/channels/{channel_id}/messages",
                form = form,
            )

        return Message(self.connection, payload)

    async def edit_member(
        self, member: Member, payload: Dict[str, Any], reason: Optional[str] = UNDEFINED
    ):
        kwargs = {}
        kwargs["json"] = payload
        if reason != UNDEFINED:
            kwargs["reason"] = reason
        await self.request(
            "PATCH", f"/guilds/{member.guild.id}/members/{member.id}", **kwargs
        )
