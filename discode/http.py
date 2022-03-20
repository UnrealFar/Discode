from __future__ import annotations

__all__ = ("HTTP",)

import asyncio
import json
import aiohttp
import logging

from urllib.parse import quote as _quote

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Literal

from .connection import Connection
from .dataclasses import Embed, File
from .models import ClientUser, Member, Message
from .utils import UNDEFINED

if TYPE_CHECKING:
    from .client import Client

aiohttp.hdrs.WEBSOCKET = "websocket"  # type: ignore

_logger = logging.getLogger("discode")


async def json_or_text(response: aiohttp.ClientResponse) -> str:
    try:
        return await response.json()
    except:
        await response.text(encoding="utf-8")


class HTTP:
    BASE_URL = "https://discord.com/api/v10"

    def __init__(
        self,
        client,
    ):
        self.client: Client = client
        self.ratelimiter = Ratelimiter(self)

    @property
    def connection(self) -> Connection:
        return self.client._connection

    async def request(
        self,
        method: str,
        path: str,
        *,
        form: Optional[List[Dict[str, Any]]] = UNDEFINED,
        parameters: Dict[str, Any] = UNDEFINED,
        **kwargs,
    ) -> Any:
        if parameters == UNDEFINED:
            parameters = dict()
        route = Route(method, path, **parameters)
        url = route.url
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
        if kwargs.get("reason"):
            headers["X-Audit-Log-Reason"] = _quote(
                kwargs.pop("X-Audit-Log-Reason"), safe="/ "
            )
        kwargs["headers"] = headers

        path_lock = self.ratelimiter._get_path_lock(path)
        unlock = True
        await self.ratelimiter.wait_until_global_reset()
        await path_lock.acquire()

        for t in range(5):
            async with self._session.request(method, url, **kwargs) as req:
                data = await json_or_text(req)
                status = req.status
                h = req.headers
                remaining = str(h.get("X-Ratelimit-Remaining"))
                bucket_hash = h.get("X-Ratelimit-Bucket")

                if bucket_hash:
                    self.ratelimiter._set_bucket(path, bucket_hash)

                if remaining == "0" and status != 429:
                    retry_after = float(h["X-Ratelimit-Reset-After"])
                    fmt = f"Request limit for path: {path!r} has been exhausted. Delaying this request by {retry_after}seconds."
                    _logger.warning(fmt)
                    unlock = False
                    await asyncio.sleep(retry_after)

                if 300 > status >= 200:
                    path_lock.release()
                    return await req.json()

                elif status == 429:
                    if not h.get("Via") is None:
                        raise Exception(data.get("message"))

                    _global = data.get("global", False)
                    retry_after = data.get("retry_after")
                    if _global:
                        _logger.critical(
                            f"Global rate limit has been hit. Retrying in {retry_after} seconds.",
                        )
                        self.ratelimiter._set_global()
                    else:
                        fmt = f"We are being rate limited. Retrying in {retry_after} seconds."
                        _logger.critical(fmt)

                    await asyncio.sleep(retry_after)
                    _logger.debug("Done sleeping for the rate limit. Retrying...")
                    if _global:
                        _logger.debug(
                            "Global rate limit is now over. Continuing operations..."
                        )
                        self.ratelimiter._free_global()
                    continue
                else:
                    raise Exception(data.get("message"))
            if unlock and path_lock is not None:
                if path_lock.locked():
                    path_lock.release()

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
            kwargs["embeds"] = [
                embed.to_dict(),
            ]

        if len(embeds) > 0:
            kwargs["embeds"] = kwargs.pop("embeds") if "embeds" in kwargs else list()
            for emb in embeds:
                kwargs["embeds"].append(emb.to_dict())

        if len(files) == 0 and file == UNDEFINED:
            payload = await self.request(
                "POST",
                "/channels/{channel_id}/messages",
                parameters={"channel_id": channel_id},
                json=kwargs,
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
                        "content_type": "application/octet-stream",
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
                "/channels/{channel_id}/messages",
                form=form,
                parameters={"channel_id": channel_id},
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
            "PATCH",
            "/guilds/{guild_id}/members/{member_id}",
            parameters={"guild_id": member.guild.id, "member_id": member.id},
            **kwargs,
        )


class Route:  # ty @nerdguyahmad
    __slots__ = (
        "method",
        "path",
        "params",
        "channel_id",
        "guild_id",
        "webhook_id",
        "webhook_token",
    )

    def __init__(
        self,
        method: Literal["GET", "POST", "PATCH", "DELETE"],
        path: str,
        **parameters: Any,
    ):
        self.method = method
        self.path = path
        self.params = parameters

        self.channel_id: Optional[int] = parameters.get("channel_id", None)
        self.guild_id: Optional[int] = parameters.get("guild_id", None)
        self.webhook_id: Optional[int] = parameters.get("webhook_id", None)
        self.webhook_token: Optional[str] = parameters.get("webhook_token", None)

    @property
    def url(self) -> str:
        return f"{HTTP.BASE_URL}{self.path.format_map({k: _quote(v) if isinstance(v, str) else v for k, v in self.params.items()})}"


class Ratelimiter:
    def __init__(self, http: HTTP):
        self.http: HTTP = http

        _global_cleared = asyncio.Event()
        _global_cleared.set()
        self._global_cleared: asyncio.Event = _global_cleared
        self.locks: Dict[str, asyncio.Lock] = {}
        self.buckets: Dict[str, str] = {}

    def _set_global(self):
        return self._global_cleared.clear()

    def _free_global(self):
        return self._global_cleared.set()

    async def wait_until_global_reset(self):
        return await self._global_cleared.wait()

    def _get_path_lock(self, path: str) -> asyncio.Lock:
        key = self.buckets.get(path, path)

        if key in self.locks:
            return self.locks[key]
        else:
            self.locks[key] = asyncio.Lock()
            return self.locks[key]

    def _set_bucket(self, path: str, bucket_hash: str):
        lock = self.locks.pop(path, None)
        if lock == None:
            lock = asyncio.Lock()

        self.locks[bucket_hash] = lock
        self.buckets[path] = bucket_hash
