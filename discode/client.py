import asyncio
from typing import Optional, Callable

from ._http import HTTP
from .user import ClientUser

__all__ = ("Client",)

class Client:
    r"""Represents the client that connects to the Discord API and the Gateway

    Parameters
    -----------
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        The :class:`asyncio.AbstractEventLoop` to be used for asynchronous functions.

    Attributes
    -----------
    loop: :class:`asyncio.AbstractEventLoop`
        The :class:`asyncio.AbstractEventLoop` to be used for asynchronous functions.
    ws: :class: `DiscordWS`
        The :class: `DiscordWS` to be used for connectiong to the gateway.
    """

    def __init__(self,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 **kwargs
    ):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        self.__events: dict = {}
        self.intents = kwargs.get("intents", 0)

    @property
    def user(self):
        return self.__user

    async def dispatch(self, event: str, *args, **kwargs):
        _event = self.__events.get(event, None)
        if _event is not None:
            await _event(*args, **kwargs)

    def on_event(self, name: str):
        def decorator(func: Callable):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("Event must be a coroutine!")

            self.__events[name] = func

        return decorator

    async def __start(self, token: str):
        self.token = token.strip()
        loop = self.loop
        self.http = HTTP(
            loop = loop,
            client = self,
            intents = self.intents
        )

        self.__user: ClientUser = await self.http.login(self.token)

        await self.http.connect()

        await self.http.close()

    def start(self, token):
        self.loop.run_until_complete(self.__start(token))
