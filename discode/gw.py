import websockets
import asyncio
import json
import sys
import time
from collections import namedtuple

from .message import Message
from .intents import Intents
from .guild import Guild
from .member import Member

EventListener = namedtuple("EventListner", "event future")

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
        self.calls = []

    async def reset(self):
        while True:
            await asyncio.sleep(0.51)
            try:
                self.calls.pop(0)
            except:
                pass

    async def new_call(self):
        self.calls.append("")

    def is_ratelimited(self) -> bool:
        if len(self.calls) >= 2:
            return True
        return False

class WS:
    def __init__(self, data):
        self.data = data
        self.loop = data.get("loop")
        self.http = data.get("http")
        self.session = self.http.session
        self.token = data.get("token")
        self.intents: Intents = data.get("intents") or Intents.default()
        self.message_cache = self.http.client.message_cache
        self.guilds = self.http.client.guilds
        self.ratelimiter = RateLimiter(ws = self, http = self.http)
        self._ready = asyncio.Event(loop=self.loop)
        self._last_send = 0
        self._last_ack = 0
        self._event_listeners = []

    def get_latency(self):
        return self._last_ack - self._last_send

    @property
    def is_closed(self) -> bool:
        return self.ws.closed

    @property
    def is_ratelimited(self) -> bool:
        return self.ratelimiter.is_ratelimited()
    
    @property
    def is_ready(self):
        return self._ready.is_set()


    async def dispatch(self, *args, **kwargs):
        _dispatch = self.data.get("dispatch")
        self.loop.create_task(_dispatch(*args, **kwargs))

    async def _get_gateway(self):
        _data = await self.http.request("GET", "/gateway")
        return _data.get("url") or "wss://gateway.discord.gg/"

    def receive(self, event):
        future = self.loop.create_future()
        listener = EventListener(event, future)
        self._event_listeners.append(listener)
        return future

    async def reconnect(self):
        try:
            await self.ws.close(code = 4002)
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
                    "seq": self.seq,
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
        self.loop.create_task(coro = self.ratelimiter.reset(), name = "RateLimitReseter")
        await self.listen()
    

    async def wait_until_ready(self) -> None:
        await self._ready.wait()

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

    async def _send(self, data):
        while True:
            if not self.is_ratelimited:
                break
            pass
        await self.ws.send(data)
        await self.ratelimiter.new_call()

    async def send(self, data):
        self.loop.create_task(self._send(str(data)))

    async def send_json(self, data):
        data = json.dumps(data)
        await self.send(data)

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
                self._last_ack = time.perf_counter()

            elif op == OP.DISPATCH:
                if event == "READY":
                    self.session_id = data["d"].get("session_id")
                    self._ready.set()
                    await self.dispatch("ready")

                elif event == "MESSAGE_CREATE":
                    msgdata = data["d"]
                    msgdata["http"] = self.http
                    message = Message(**msgdata)
                    self.message_cache[message.id] = message
                    if len(self.message_cache) == self.http.client.message_limit:
                        temp = list(self.message_cache)[0]
                        self.message_cache.pop(temp)
                    await self.dispatch("message", message)

                elif event == "MESSAGE_UPDATE":
                    msg = self.message_cache.get(int(data["d"]["id"]), None)
                    if msg is not None:
                        beforedata = msg.data
                        before = Message(**beforedata)
                        msg.data["content"] = data["d"].get("content")
                        msg.data["edited_at"] = data["d"].get("edited_timestamp")
                        after = msg
                        await self.dispatch("message edit", before, after)

                elif event == "GUILD_CREATE":
                    gdata = data.get("d")
                    if self.http.client.chunk_guilds_at_startup:
                        await self.chunk_guild(int(gdata.get("id")))

                    gdata["http"] = self.http
                    del gdata["members"]
                    guild = Guild(**gdata)
                    self.guilds[int(gdata.get("id"))] = guild

                elif event == "GUILD_MEMBERS_CHUNK":
                    guild = self.guilds[int(data.get("d").get("guild_id"))]
                    for member in data.get("d").get("members"):
                        member["http"] = self.http
                        mem = Member(**member)
                        try:
                            guild._members.append(mem)
                        except:
                            guild._members = [mem]

    @property
    def hb_payload(self):
        return {"op": OP.HEARTBEAT, "d": self.seq}

    async def heartbeat(self, interval: float):
        while True:
            if self._last_ack > (time.perf_counter() + 5):
                await self.reconnect()

            await self.send_json(self.hb_payload)
            self._last_send = time.perf_counter()
            await asyncio.sleep(interval)

    async def chunk_guild(self, _id: int, *, query: str = "", limit: int = 0, presences: bool = False, nonce = None):
        payload = {
            "op": OP.REQUEST_MEMBERS,
            "d": {
                "guild_id": str(_id),
                "query": query,
                "limit": limit,
            },
        }
        if nonce:
            payload["d"]["nonce"] = nonce
        if presences:
            payload["presenses"] = presences
        return await self.http.ws.send_json(payload)
