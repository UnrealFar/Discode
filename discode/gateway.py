from __future__ import annotations

import asyncio
import json
import sys
import time
import zlib
from typing import Callable, Dict, List, NamedTuple, Union, Optional

import aiohttp
import logging

from .connection import Connection
from .enums import GatewayEvent
from .models import Guild, Message

_logger = logging.getLogger("discode")

class OP:
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE = 3
    VOICE_STATE = 4
    VOICE_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
    GUILD_SYNC = 12


class Shard:
    def __init__(self, client, url: str, *, shard_id: Optional[int] = None):
        self.client = client
        self.http = client._http
        self.connection = client._connection
        self.loop: asyncio.AbstractEventLoop = client.loop
        self.lock: asyncio.Lock = asyncio.Lock()
        self.handler: SocketHandler = SocketHandler(self)
        self.shard_id: Optional[int] = shard_id
        self.running: bool = False

        self.token: str = client.token
        self.intents = client.intents
        self.sequence: int = None
        self.session: aiohttp.ClientSession = self.http._session
        self.options = {}
        self.inflator = zlib.decompressobj()
        self.buffer = bytearray()
        self.ZLIB_SUFFIX = b"\x00\x00\xff\xff"
        self._last_send: float = None
        self.url: str = url

    @property
    def latency(self) -> float:
        return self.handler.latency

    def is_ratelimited(self) -> bool:
        if self._last_send:
            return (time.perf_counter() - self._last_send) < 0.5
        return False

    def _get_gateway_url(self, compress=True, v=9) -> str:
        url = self.url
        url = f"{url}?encoding=json&v={v}"
        if compress:
            url = f"{url}&compress=zlib-stream"
        return url

    async def identify(self):
        await self.send_json(
            {
                "op": OP.IDENTIFY,
                "d": {
                    "token": self.token,
                    "intents": int(self.intents),
                    "compress": self.options.get("compress", True),
                    "properties": {
                        "$os": sys.platform,
                        "$browser": "discode",
                        "$device": "discode",
                    },
                    "shard": (self.shard_id, self.client.shard_count)
                },
            }
        )
        _logger.info("The gateway has sent the identify payload.")

    async def heartbeat(self):
        self.handler.last_hb = time.perf_counter()
        await self.send_json({"op": OP.HEARTBEAT, "d": self.sequence})
        _logger.info("Keeping SHARD %s alive with sequence %s", self.shard_id, self.sequence)

    async def heartbeat_task(self, interval: float):
        while True:
            await self.heartbeat()
            await asyncio.sleep(interval)

    async def connect(self, version=9, compress=True, reconnect=True):
        self.options["version"] = version
        self.options["reconnect"] = reconnect
        self.options["compress"] = compress
        url = self._get_gateway_url(compress, version)
        self.ws = await self.session.ws_connect(url)
        await self.start()

    async def receive(self) -> dict:
        data = await self.ws.receive()
        data = data.data
        if not data:
            return

        if isinstance(data, bytes):
            self.buffer.extend(data)

            if len(data) < 4 or data[-4:] != self.ZLIB_SUFFIX:
                self.buffer = bytearray()
                return

            data = self.inflator.decompress(self.buffer)
            data = data.decode("utf-8")
            self.buffer = bytearray()

        if isinstance(data, int):
            raise TypeError(f"Received an int: {data}")

        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return
        return data

    async def block_send(self):
        if self.is_ratelimited():
            async with self._lock:
                while True:
                    if not self.is_ratelimited():
                        break
            self._last_send = time.perf_counter()

    async def send(self, data: str):
        await self.block_send()
        await self.ws.send_str(str(data))

    async def send_json(self, payload: dict):
        payload = json.dumps(payload)
        await self.send(payload)

    async def start(self):
        await self.identify()
        self.running = True
        while True:
            recv = await self.receive()
            self.loop.create_task(self.handler.handle_events(recv))


class SocketHandler:
    def __init__(self, shard: Shard):
        self.shard: Shard = shard
        self.last_hb: int = int()
        self.latency: float = float("inf")
        self.connection: Connection = shard.connection
        self.loop: asyncio.AbstractEventLoop = shard.loop
        self.waiting_guilds: dict = {}

    async def dispatch(self, event, *args, **kwargs):
        await self.shard.client.dispatch(event, *args, **kwargs)
        await self.check(event, *args, **kwargs)

    async def handle_events(self, payload: dict):
        if not isinstance(payload, dict):
            return
        shard = self.shard
        connection = self.connection
        shard.sequence = payload['s'] if 's' in payload else shard.sequence
        op = payload.get("op")
        data = payload.get("d")
        t = str(payload.get("t")).lower()

        if op == OP.HELLO:
            interval = data.get("heartbeat_interval") / 1000
            self.hb_task = self.loop.create_task(shard.heartbeat_task(interval))

        elif op == OP.HEARTBEAT_ACK:
            self.latency = time.perf_counter() - self.last_hb
            if self.latency > 10:
                _logger.critical("High websocket latency. Shard ID %s is %.1fs behind.")

        elif op == OP.DISPATCH:
            await self.dispatch(GatewayEvent.DISPATCH, payload)

            if t == GatewayEvent.READY:
                unavailable_guilds = data.pop("guilds", [])
                for ug in unavailable_guilds:
                    if "id" not in ug:
                        continue
                    ug_id = int(ug["id"])
                    fut = self.loop.create_future()
                    self.waiting_guilds[ug_id] = fut
                    try:
                        await asyncio.wait_for(fut, timeout=2)
                    except asyncio.TimeoutError:
                        pass
                await self.dispatch(GatewayEvent.READY)

            elif t == GatewayEvent.MESSAGE_CREATE:
                message = Message(connection, data)
                connection.message_cache[message.id] = message
                if not message.guild:
                    ch = connection.channel_cache.get(message.channel_id)
                    if not ch:
                        try:
                            dm = await message.author.create_dm()
                            connection.channel_cache[dm.id] = dm
                        except:
                            pass
                await self.dispatch(GatewayEvent.MESSAGE_CREATE, message)

            elif t == GatewayEvent.MESSAGE_UPDATE:
                before = connection.message_cache.get(int(data["id"]))
                if before is not None:
                    after = before.copy(**data)
                    connection.message_cache[after.id] = after
                    await self.dispatch(GatewayEvent.MESSAGE_UPDATE, before, after)

            elif t == GatewayEvent.GUILD_CREATE:
                guild = Guild(connection, data)
                if guild.id in self.waiting_guilds:
                    fut: asyncio.Future = self.waiting_guilds[guild.id]
                    try:
                        fut.set_result(0)
                        self.waiting_guilds.pop(guild.id, None)
                    except asyncio.InvalidStateError:
                        pass
                connection.add_guild(guild)
                await self.dispatch(GatewayEvent.GUILD_CREATE, guild)

            elif t == GatewayEvent.GUILD_UPDATE:
                after = Guild(connection, data)
                before = connection.get_guild(after.id)
                connection.add_guild(after)
                await self.dispatch(GatewayEvent.GUILD_UPDATE, before, after)

            elif t == GatewayEvent.GUILD_DELETE:
                if data.pop("unavailable", True):
                    fut = self.waiting_guilds.pop(int(data.pop("id", 0)), None)
                    if isinstance(fut, asyncio.Future):
                        fut.cancel()
                else:
                    await self.dispatch(
                        GatewayEvent.GUILD_DELETE,
                        self.connection.remove_guild(int(data.pop("id", 0))),
                    )

    async def check(self, event: str, *args, **kwargs):
        client = self.shard.client
        for listener in client._dispatch_listeners:
            if listener.event == event:
                check = listener.check
                if asyncio.iscoroutinefunction(check):
                    result = await check(*args, **kwargs)
                else:
                    result = check(*args, **kwargs)
                if result:
                    listener.future.set_result(0)
                    client._dispatch_listeners.remove(listener)


class DispatchListener(NamedTuple):

    event: str
    future: asyncio.Future
    check: Callable
