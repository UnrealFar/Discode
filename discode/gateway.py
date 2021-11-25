import aiohttp
from typing import Optional
import asyncio

class OP:
    DISPATCH        = 0
    HEARTBEAT       = 1
    IDENTIFY        = 2
    PRECENSE        = 3
    VOICE_STATE     = 4
    VOICE_PING      = 5
    RESUME          = 6
    RECONNECT       = 7
    REQUEST_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO           = 10
    HEARTBEAT_ACK   = 11

class DiscordWS:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        session: aiohttp.ClientSession
    ):
        
        self.loop = loop
        self.session = session