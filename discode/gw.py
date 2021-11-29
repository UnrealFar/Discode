import zlib
import websockets
import asyncio
import json
import sys
import time

from .message import Message
from .intents import Intents
from .guild import Guild
from .errors import InvalidToken


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

class RateLimiter:
    def __init__(self, **kwargs):
        pass

class WS:
    def __init__(self, data):
        self.data = data
        self.loop = data.get("loop")
        self.http = data.get("http")
        self.session = self.http.session
        self.token = data.get("token")
        self.__latency = 0
        self.last_hb_ack = 0
        self.intents: Intents = data.get("intents") or Intents.default()
        self.message_cache = self.http.client.message_cache
        self.guild_cache = self.http.client.guild_cache

    @property
    def latency(self):
        self.loop.create_task(self.ping())
        return self.__latency

    @property
    def is_closed(self):
        return self.ws.closed

    async def dispatch(self, *args, **kwargs):
        _dispatch = self.data.get("dispatch")
        self.loop.create_task(_dispatch(*args, **kwargs))

    async def _get_gateway(self):
        _data = await self.http.request("GET", "/gateway")
        return _data.get("url") or "wss://gateway.discord.gg/"

    async def reconnect(self):
        try:
            await self.ws.close()
        except:
            pass
        _gateway_url = await self._get_gateway()
        self.ws = await websockets.connect(_gateway_url)
        await self.send_json(
            {
                "op": OP.RECONNECT,
                "d": {
                    "token": self.token,
                    "session_id": self.session_id,
                    "seq": self.seq
                }
            }
        )

    async def get_ws(self):
        _gateway_url = await self._get_gateway()
        ws = await websockets.connect(_gateway_url)
        return ws

    async def handle(self):
        self.ws = await self.get_ws()
        self.seq = None
        await self.listen()

    async def identify(self):
        data = {
            "op": OP.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents.value,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "discode",
                    "$device": "discode",
                },
                "encoding": "json",
                "v": 9,
            },
        }

        await self.send_json(data)
        await self.ping()

    async def send(self, data):
        await self.ws.send(str(data))

    async def send_json(self, data):
        data = json.dumps(data)
        await self.send(data)

    async def ping(self):
        oldtime = time.perf_counter()
        pong = await self.ws.ping()
        await pong
        newtime = time.perf_counter()
        self.__latency = newtime - oldtime
    

    async def listen(self):
        async for data in self.ws:
            data = json.loads(data)
            seq = data.get("s")
            event = data.get('t')
            op = data.get('op')
            if seq is not None:
                self.seq = seq

            if op == OP.HELLO:
                interval = data["d"]["heartbeat_interval"] / 1000.0
                self.loop.create_task(self.heartbeat(interval))
                await self.identify()

            elif op == OP.INVALID_SESSION:
               raise Exception("Invalid Token")

            elif op == OP.HEARTBEAT:
                await self.send_json(self.hb_payload)

            elif op == OP.HEARTBEAT_ACK:
                self.last_hb_ack = time.perf_counter()

            elif op == OP.DISPATCH:
                if event == "READY":
                    self.session_id = data["d"].get("session_id")
                    await self.dispatch("ready")

                elif event == "MESSAGE_CREATE":
                    msgdata = data["d"]
                    msgdata["http"] = self.http
                    message = Message(self.loop, data=msgdata)
                    self.message_cache[message.id] = message
                    if len(self.message_cache) == self.http.client.message_limit:
                        temp = list(self.message_cache)[0]
                        self.message_cache.pop(temp)
                    await self.dispatch("message", message)

                elif event == "MESSAGE_UPDATE":
                    msg = self.message_cache.get(data["d"]["id"], None)
                    if msg is not None:
                        beforedata = msg.data
                        before = Message(loop=self.loop, data=beforedata)
                        after = msg
                        after.content = data["d"].get("content")
                        after.edited_at = data["d"].get("edited_timestamp")
                        self.message_cache[data["d"].get("id")] = after
                        await self.dispatch("message edit", before, after)

                elif event == "GUILD_CREATE":
                    gdata = data.get("d")

                    guild = Guild(gdata, loop=self.loop, http=self.http)
                    self.guild_cache[int(gdata.get("id"))] = guild

    @property
    def hb_payload(self):
        return {"op": OP.HEARTBEAT, "d": self.seq}

    async def heartbeat(self, interval: float):
        while True:
            if self.last_hb_ack > (interval + 10):
                await self.reconnect()

            await self.send_json(self.hb_payload)
            await asyncio.sleep(interval)
