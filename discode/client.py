import asyncio
import aiohttp

from typing import Union, Optional, Any, Dict, List

from .connection import Connection
from .gateway import Gateway
from .flags import Intents
from .enums import GatewayEvent
from .http import HTTP
from .models import Guild, User, ClientUser, Message

class Client:

    r"""Represents the Client that connects to the Discord Gateway and HTTP Api."""

    def __init__(
        self,
        token: str,
        *,
        intents: Intents = None,
        loop: asyncio.AbstractEventLoop = None
    ):
        self.token: str = token.strip()
        self.loop: asyncio.AbstractEventLoop = (
            loop if loop else asyncio.get_event_loop()
        )
        self.intents: Intents = intents if intents else Intents.all()
        self._http: HTTP = HTTP(self)
        self._connection: Connection = Connection(self)
        self._listeners: Dict[str, Any] = {}

    @property
    def user(self) -> ClientUser:
        return self._user

    @property
    def users(self) -> List[User]:
        return [u for u in self._connection.user_cache.values()]

    @property
    def guilds(self) -> List[Guild]:
        return [g for g in self._connection.guild_cache.values()]

    @property
    def messages(self) -> List[Message]:
        return [g for g in self._connection.message_cache.values()]

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._http._session

    async def run_task(self, **kwargs):
        self._user = await self._http.login()
        ws_options = kwargs.pop("ws_options", {})
        self._ws: Gateway = Gateway(self)
        await self._ws.connect(**ws_options)

    def run(self, *args, **kwargs):
        loop = self.loop

        async def runner():
            await self.run_task(*args, **kwargs)

        def stop(f):
            asyncio.ensure_future(self.close())
            loop.stop()

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            future.remove_done_callback(stop)

    async def close(self):
        await self._http.logout()
        await self._http.close()

    def on_event(self, event: Union[str, GatewayEvent]):
        def wrapper(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"Couldn't register {func} as a listener as it was of type {type(func)} and the library expected a coroutine!")
            self.add_listener(func, event)
        return wrapper

    def add_listener(self, coro, event):
        if event not in vars(GatewayEvent).values():
            raise Exception(f"Invalid Listener: {event}")
        if event in self._listeners:
            self._listeners.append(coro)
        else:
            self._listeners[event] = [coro]

    async def dispatch(
        self,
        event,
        *args,
        **kwargs
    ):
        ev = getattr(self, f"on_{event}", None)
        if asyncio.iscoroutinefunction(ev):
            await ev(*args, **kwargs)
        listeners = self._listeners.get(event, [])
        for l in listeners:
            self.loop.create_task(l(*args, **kwargs))

