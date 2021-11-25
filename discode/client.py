import asyncio
from typing import Optional, Callable

from .gateway import DiscordWS
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


    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        self.__events: dict = {}

    @property
    def user(self):
        return self.__user
    
    async def dispatch(self, event: str, *args, **kwargs):
        _event = self.__events.get(event, None)
        if _event is not None:
            await _event(*args, **kwargs)

    def event(self, func: Callable):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Event must be a coroutine!")

        self.__events[func.__name__[3:]] = func

    def start(self, token: str):
        self.token = token.strip()
        loop = self.loop
        self.http = HTTP(
            loop = loop
        )
        self.__user: ClientUser = self.loop.run_until_complete(self.http.login(self.token))

        self.loop.run_until_complete(
            self.dispatch("ready")
            )
        
        self.loop.run_until_complete(self.http.close())