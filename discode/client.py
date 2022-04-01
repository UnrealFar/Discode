from __future__ import annotations

__all__ = ("Client",)

import asyncio
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union, TypeVar

import aiohttp
import logging

from . import utils
from .connection import Connection
from .enums import GatewayEvent
from .flags import Intents, Permissions
from .gateway import Shard, DispatchListener
from .http import HTTP
from .models import ClientUser, DMChannel, Guild, Message, TextChannel, User

Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])

_logger = logging.getLogger("discode")

class Client:

    r"""
    Represents the Client that connects to the Discord Gateway and HTTP Api.

    Parameters
    ----------

    token: :class:`str`
        The token to use to communicate with the gateway and REST APIs.
    intents: :class:`Intents`
        The intents to use while connecting to the gateway. Defaults to :meth:`Intents.all()`.
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop the client should use for asynchronous operations.

    Attributes
    ----------

    token: :class:`str`
        The token used to connect to the REST & gateway APIs.
    intents: :class:`Intents`
        The intents the client is using.
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop used by the client for asynchronous operations.
    """

    def __init__(
        self,
        token: str,
        *,
        intents: Optional[Intents] = None,
        api_version: Optional[int] = 10,
        shard_count: Optional[int] = None,
        gateway_timeout: Optional[int] = 5
    ):
        if shard_count is not None and shard_count < 1:
            raise ValueError("Number of shards must be greater than or equal to 1.")
        self.token: str = token.strip()
        self.loop: asyncio.AbstractEventLoop = None
        self.intents: Intents = intents if intents else Intents.all()
        self.api_version: int = int(api_version)
        self._http: HTTP = HTTP(self)
        self._connection: Connection = Connection(self)
        self._http.connection = self._connection
        self._listeners: Dict[str, Any] = {}
        self._dispatch_listeners: List[DispatchListener] = []
        self._shards: Dict[int, Shard] = {}
        self._ready: asyncio.Event = asyncio.Event()
        self.shard_count: Optional[int] = shard_count
        self.max_concurrency: Optional[int] = None
        self.gatewat_timeout: float = gateway_timeout
        self.__closed: asyncio.Event = None

    @property
    def latency(self) -> float:
        r""":class:`float`: The average latency of the websocket connection over all the shards."""
        latencies = tuple(s.latency for s in self._shards.values())
        return sum(latencies) / len(self._shards)

    @property
    def is_ready(self) -> bool:
        r":class:`bool` Whether the client is completely ready for use or no."
        return self._ready.is_set()

    @property
    def user(self) -> ClientUser:
        r""":class:`ClientUser`: The user object belonnging to the client."""
        return getattr(self, "_user", None)

    @property
    def users(self) -> List[User]:
        r"""List[:class:`User`]: A list of all the users the client can see."""
        return list(self._connection.user_cache.values())

    @property
    def guilds(self) -> List[Guild]:
        r"""List[:class:`Guild`]: A list of all the guilds visible to the client."""
        return list(self._connection.guild_cache.values())

    @property
    def messages(self) -> List[Message]:
        r"""List[:class:`Message`]: A list of all the messages cached by the client."""
        return list(self._connection.message_cache.values())

    @property
    def channels(self) -> List[Union[TextChannel, DMChannel]]:
        r"""List[Union[:class:`TextChannel`, :class:`DMChannel`]]: A list of all the channels cached by the client."""
        return list(self._connection.channel_cache.values())

    @property
    def dm_channels(self) -> List[DMChannel]:
        r"""List[:class:`DMChannel`]: A list of all the direct message channels cached by the client."""
        return [c for c in self._connection.channel_cache.values() if c.type == 1]

    @property
    def invite_url(self) -> str:
        r""":class:`str`: Generates an invite url forr the client and returns it."""
        return utils.invite_url(
            client_id=self.user.id, permissions=Permissions(administrator=True)
        )

    @property
    def session(self) -> aiohttp.ClientSession:
        r""":class:`aiohttp.ClientSession`: The client session used by the http client for making requests to the Discord API."""
        return self._http._session

    async def wait_until_ready(self) -> None:
        await self._ready.wait()

    async def __dispatch_ready(self) -> None:
        for shard in self._shards.values():
            await shard._ready.wait()
        self._ready.set()
        await self.dispatch(GatewayEvent.READY)

    async def run_task(self, *args, **kwargs) -> Client:
        r"""This method is a coroutine. It is used to start the client, i.e., connect to gateway API and the REST API.
        It prepares the client completely.

        Returns
        -------
        :class:`Client`
            The client itself.
        """
        self.loop = utils.get_event_loop()
        self.__closed = asyncio.Event(loop = self.loop)
        self._user = await self._http.login()
        ws_options = kwargs.pop("ws_options", {})
        gw_data = await self._http.request("GET", "/gateway/bot")

        self.max_concurrency = gw_data['session_start_limit']['max_concurrency']

        if self.shard_count is None:
            self.shard_count = gw_data['shards']

        for g_id in range(self.shard_count):
            self._shards[g_id] = Shard(self, url = gw_data['url'], shard_id = g_id)

        shards_to_launch = list(self._shards.values())
        while len(shards_to_launch) >= 1:
            try:
                to_launch = shards_to_launch[0]
            except IndexError:
                break
            shards_to_launch.remove(to_launch)
            asyncio.create_task(to_launch.connect(**ws_options), name = f'discode:shard{to_launch._id}.connect()')

        asyncio.create_task(self.__dispatch_ready(), name='discode:client.__dispatch_ready()')

        await self.__closed.wait()
        return self

    def run(self, *args, **kwargs):
        r"""The is method is similar to :meth:`Client.run_task()` but is a normal function and not a coroutine.
        The library recommends users to use this to start the bot as this function handles closing the client without raising any errors and runs till the client is alive.

        .. warning:: Code written after this function is called will most probably not get executed till the bot stops.

        Returns
        -------
        :class:`Client`
            The client itself.
        """
        return asyncio.run(self.run_task(*args, **kwargs))

    async def close(self) -> None:
        r"""Closes the client, the http client, and the gateway connection."""
        await self._http.logout()
        await self._http.close()
        for shard in self._shards.values():
            await shard.close()
        for listener in self._ws.handler.dispatch_listeners:
            fut = listener.future
            fut.cancel()

    def on_event(self, event: Union[str, GatewayEvent]) -> Coro:
        r"""Decorator to register event listeners to the client. The function decorated must be a coroutine. This decorator uses :meth:`Client.add_listener()` to register the listener.

        Parameters
        ----------

        event: :class:`str`
            The event the listener should be registered for.
        Raises
        ------

        TypeError
            The function decorated isn't a coroutine.
        """

        def wrapper(func: Coro):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(
                    f"Couldn't register {func} as a listener as it was of type {type(func)} and the library expected a coroutine!"
                )
            self.add_listener(func, event)
            return func

        return wrapper

    def add_listener(self, coro: Coro, event: str):
        r"""This function registers a listener to the client.

        Parameters
        ----------

        coro: :class:`Coro`
            A callable coroutine.
        event: :class:`str`
            The event to which the listener should be registered to. This event must be a valid event documented under :class:`GatewayEvent`.

        Returns
        -------
        :class:`Coro`
            The coroutine passed in as a parameter.

        Raises
        ------
        TypeError
            The coro passed in parameters isn't a coroutine.
        """
        if event not in vars(GatewayEvent).values():
            raise Exception(f"Invalid Listener: {event}")
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(
                f"Couldn't register {coro} as a listener as it was of type {type(coro)} and the library expected a coroutine!"
            )
        if event in self._listeners:
            self._listeners.append(coro)
        else:
            self._listeners[event] = [coro]
        return coro

    async def dispatch(self, event, *args, **kwargs):
        ev = getattr(self, f"on_{event}", None)
        loop = self.loop
        if asyncio.iscoroutinefunction(ev):
            asyncio.ensure_future(ev(*args, **kwargs), loop = loop)
        listeners = self._listeners.get(event, [])
        for l in listeners:
            asyncio.ensure_future(l(*args, **kwargs), loop = loop)

    async def wait_for(
        self,
        event: str,
        check: Union[Callable[..., Any], Coro],
        *,
        timeout=30,
    ):
        r"""Waits for a dispatch event from the websocket.

        This method can be used to wait for a user to send a message that matches the passed check.

        Parameters
        ----------
        event: :class:`str`
            The event to wait for. Must be a valid event documented under :class:`GatewayEvent`.
        check: Union[Callable[True], Coro]
            The check that should be run on the event. Can either be a normal function or a coroutine, with valid parameters specified under :class:`GatewayEvent`. Must return :class:`True` if the check is successful.

        Returns
        -------
        :class:`asyncio.Future`
            The future created to wait for the event.

        Raises
        ------
        :class:`asyncio.TimeoutError`
            The timeout has finished.
        """
        event = event.lower()
        fut = self.loop.create_future()
        listener = DispatchListener(event=event, future=fut, check=check)
        self._dispatch_listeners.append(listener)
        fut = listener.future
        try:
            return await asyncio.wait_for(fut, timeout=timeout)
        except asyncio.TimeoutError as exc:
            fut.cancel()
            raise exc
