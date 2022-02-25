
from __future__ import annotations

import asyncio
import aiohttp
import json, zlib
import sys, time

from .enums import GatewayEvent
from .connection import Connection
from .models import Guild, Message

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

class Gateway:

    def __init__(
        self,
        client
    ):
        self.client = client
        self.http = client._http
        self.connection = client._connection
        self.loop: asyncio.AbstractEventLoop = client.loop
        self.handler: SocketHandler = SocketHandler(self)

        self.token: str = client.token
        self.intents = client.intents
        self.sequence: int = None
        self.session: aiohttp.ClientSession = self.http._session
        self.options = {}
        self.inflator = zlib.decompressobj()
        self.buffer = bytearray()
        self.ZLIB_SUFFIX = b'\x00\x00\xff\xff'

    @property
    def latency(self) -> float:
        return self.handler.latency

    async def _get_gateway(self, compress = True, v = 9) -> str:
        data = await self.http.request("GET", "/gateway")
        url = data.get("url")
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
                        "$device": "discode"
                    }
                }
            }
        )

    async def heartbeat(self):
        self.handler.last_hb = time.perf_counter()
        await self.send_json({"op": OP.HEARTBEAT, "d": self.sequence})

    async def heartbeat_task(self, interval: float):
        while True:
            await self.heartbeat()
            await asyncio.sleep(interval)

    async def connect(self, version = 9, compress = True, reconnect = True):
        self.options["version"] = version
        self.options["reconnect"] = reconnect
        self.options["compress"] = compress
        url = await self._get_gateway(compress, version)
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

    async def send(self, data: str):
        await self.ws.send_str(str(data))

    async def send_json(self, payload: dict):
        payload = json.dumps(payload)
        await self.send(payload)

    async def start(self):
        await self.identify()
        while True:
            recv = await self.receive()
            self.loop.create_task(self.handler.handle_events(recv))

class SocketHandler:

    def __init__(self, gateway: Gateway):
        self.gateway: Gateway = gateway
        self.last_hb: int = int()
        self.latency: float = float("inf")
        self.connection: Connection = gateway.connection
        self.loop: asyncio.AbstractEventLoop = gateway.loop
        self.waiting_guilds: dict = {}

    @property
    def dispatch(self):
        return self.gateway.client.dispatch

    async def handle_events(self, payload: dict):
        if not isinstance(payload, dict):
            return
        gateway = self.gateway
        client = gateway.client
        connection = self.connection
        gateway.sequence = payload.get("s")
        op = payload.get("op")
        data = payload.get("d")
        t = str(payload.get("t")).lower()

        if op == OP.HELLO:
            interval = data.get("heartbeat_interval") / 1000
            self.hb_task = self.loop.create_task(gateway.heartbeat_task(interval))

        elif op == OP.HEARTBEAT_ACK:
            self.latency = time.perf_counter() - self.last_hb

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
                        await asyncio.wait_for(fut, timeout = 2)
                    except asyncio.TimeoutError:
                        pass
                await self.dispatch(GatewayEvent.READY)

            elif t == GatewayEvent.MESSAGE_CREATE:
                message = Message(connection, data)
                connection.message_cache[message.id] = message
                if not message.guild:
                    ch = connection.channel_cache.get(message.channel_id)
                    if not ch:
                        dm = await message.author.create_dm()
                        connection.channel_cache[dm.id] = dm
                await self.dispatch(GatewayEvent.MESSAGE_CREATE, message)

            elif t == GatewayEvent.GUILD_CREATE:
                guild = Guild(connection, data)
                if guild.id in self.waiting_guilds:
                    fut: asyncio.Future= self.waiting_guilds[guild.id]
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
                    await self.dispatch(GatewayEvent.GUILD_DELETE, self.connection.remove_guild(int(data.pop("id", 0))))
