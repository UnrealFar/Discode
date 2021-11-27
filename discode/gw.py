import websockets
import asyncio
import threading
import json
import sys
import random

from .message import Message

class OP:
    DISPATCH = 0
    IDENTIFY = 2
    HEARTBEAT = 1
    HELLO = 10

class WS:
    def __init__(self, data):
        self.loop = data.get("loop")
        self.http = data.get("http")
        self.dispatch = data.get("dispatch")
        self.session = self.http.session
        self.token = data.get("token")
        self.intents = data.get("intents", 0)
        self.message_cache= self.http.client.message_cache

    async def get_ws(self):
        ws = await websockets.connect(
            "wss://gateway.discord.gg/?v=9&encoding=json"
        )
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
                "intents": self.intents,
                "properties": {
                  "$os": sys.platform,
                  '$browser': 'discode',
                  '$device': 'discode',
                }
            }
        }

        await self.send_json(data)

    async def send(self, data):
        await self.ws.send(str(data))

    async def send_json(self, data):
        data = json.dumps(data)
        await self.send(data)

    async def listen(self):
        async for data in self.ws:
            data = json.loads(data)
            seq = data.get("s")
            if seq is not None:
                self.seq = seq
            if data["op"] != OP.DISPATCH:
                if data["op"] == OP.HELLO:
                    interval = (
                        data["d"]["heartbeat_interval"] / 1000.0
                    )
                    self.loop.create_task(self.heartbeat(interval))
                    await self.identify()

            if data["op"] == OP.DISPATCH:
                if data["t"] == "READY":
                    self.session_id = data["d"].get("session_id")
                    await self.dispatch("ready")

                if data["t"] == "MESSAGE_CREATE":
                    msgdata = data["d"]
                    msgdata["http"] = self.http
                    message = Message(
                        self.loop,
                        data = msgdata
                    )
                    
                    self.message_cache.append(message)
                    if len(self.message_cache) == self.http.client.message_limit:
                        self.message_cache.pop(0)
                    await self.dispatch("message", message)

                if data["t"] == "MESSAGE_UPDATE":
                    for msg in self.message_cache:
                        if data["d"]["id"] == msg.id:
                            beforedata = msg.data
                            before = Message(
                                loop = self.loop,
                                data = beforedata
                            )
                            after = msg
                            after.content = data["d"]["content"]
                            after.edited_at = data["d"]["edited_timestamp"]
                            await self.dispatch("message edit", before, after)
                            break

    async def heartbeat(self, interval: float):
        while True:
            data = {
                "op": OP.HEARTBEAT,
                "d": self.seq
            }
            await self.send_json(data)
            await asyncio.sleep(interval)
