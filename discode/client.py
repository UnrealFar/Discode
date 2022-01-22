import asyncio
import traceback
import sys
from typing import Optional, Callable, List, Union

from ._http import HTTP
from .user import ClientUser
from .guild import Guild
from .activity import Activity
from .channel import Channel, TextChannel
from .member import Member
from .intents import Intents
from . import base_events

__all__ = ("Client",)


class Client:
    r"""Represents the client that connects to the Discord API and the Gateway

    Parameters
    ----------
    owner_ids: List[:class:`int`]
        The unique IDs of the owners of the bot.
    message_limit: :class:`int`
        The maximum amount of messages to have in the cache. Messages are cached to reduce api calls and prevent ratelimits.

    chunk_guilds_at_startup: :class:`bool`
        If the client should chunk up all the guild members before the ready event. Defaults to :class:`True`.

    intents: :class:`Intents` = :meth:`Intents.default()`
        The intents to use while connecting to the Discord gateway.

    Attributes
    -----------
    loop: :class:`asyncio.AbstractEventLoop`
        The :class:`asyncio.AbstractEventLoop` to be used for asynchronous functions.

    intents: :class:`Intents`
        The intents that were provide while connecting to the Discord gateway.

    guilds: List[:class:`Guild`]
        The guild cache of the client

    active_interactions: List[:class:`Any`]
        Contains all the component interactions that the client is listening for.
    """

    def __init__(
        self,
        owner_id: int = None,
        owner_ids: List[int] = None,
        message_limit: int = None,
        chunk_guilds_at_startup: bool = True,
        intents: Optional[Intents] = None,
        *args,
        **kwargs
    ):
        self.loop: asyncio.AbstractEventLoop = kwargs.get("loop", asyncio.get_event_loop())
        self.__events: dict = {}
        self.message_cache = []
        self.guilds: List[Guild] = []
        self.chunk_guilds_at_startup: bool = chunk_guilds_at_startup
        self.message_limit: Optional[int] = message_limit
        self.intents = intents if intents else Intents.default()
        self.active_interactions = []
        self.owner_id = owner_id
        self.owner_ids = [owner_id] if owner_ids == None else owner_ids
        for ev in dir(base_events):
            if ev.start

    @property
    def user(self) -> ClientUser:
        r"""Returns the :class:`ClientUser` connected to the Discord Gateway.
        """
        return self.__user
    
    @property
    def is_ready(self) -> bool:
        r"""Retruns a :class:`True` if the :class:`Client` is ready, else :class:`False`

        Returns
        -------
        :class:`bool`
            The ready state of the client.
        """
        return self.http.ws._ready.is_set()

    @property
    def latency(self) -> float:
        r"""Returns the latency of the websocket connection with the Discord Gateway.

        Returns
        -------
        :class:`float`
            The latency of the client in :class:`float`
        """
        try:
            return self.http.ws.get_latency()
        except Exception:
            return None

    async def dispatch(self, event: str, *args, **kwargs):
        if not self.is_ready and event != "ready":
            return

        events = self.__events.get(event, [])
        for _event in events:
            try:
                await _event(*args, **kwargs)
            except Exception as exception:
                if "error" in self.__events:
                    try:
                        await self.__events["error"]()
                    except Exception as err:
                        await self.error("error handler", exception = err)
                else:
                    await self.error(event, exception = exception)

    async def error(self, event, exception: Exception):
        r"""The default error handler of the client.
        """
        print(f"An error occured in \"{event}\" event", file = sys.stderr)
        traceback.print_exception(
            type(exception),
            exception,
            exception.__traceback__,
            file = sys.stderr
        )

    def on_event(self, event_name: str) -> ...:
        r"""The decorator that registers a new listener.
        """
        def decorator(func: Callable):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("Event must be a coroutine!")

            self.add_listener(
                **{
                    "event_name": event_name,
                    "callback": func
                }
            )

        return decorator

    def add_listener(self, event_name: str, callback: Callable):
        r"""This used by the :meth:`Client.on_event()` decorator to register a new listener, this can also be used to add listeners manually.
        The callback must be a coroutine.
        """

        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Listener must be a coroutine.")

        if event_name not in self.__events:
            self.__events[event_name] = []
        self.__events[event_name].append(callback)

    async def start_task(self, token: str):
        r"""A coroutine to start the bot. It is recommended to use the start method if you do not know what you are doing.
        """
        self.token = token.strip()

        loop = self.loop

        self.http = HTTP(loop=loop, client=self, intents=self.intents)

        self.__user: ClientUser = await self.http.login(self.token)

        await self.http.connect()

    def start(self, token: str):
        r"""Connects to the Discord Gateway along with the REST API.
        It is recommended to use this function to start your bot / client.
        """
        loop = self.loop
        loop.create_task(self.start_task(token))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

    def get_channel(self, channel_id: int, guild_id: int) -> Union[Channel, TextChannel]:
        r"""Get a :class:`Channel` from the client's cache. Returns :class:`None` if the channel doesnt't exist or if the cache hasn't been updated yet. In this case, :meth:`Client.fetch_channel()` can be used.

        Returns
        -------
        Union[:class:`TextChannel`, :class:`Channel`]
            Returns the channel object or :class:`None` if its not found.
        """
        guild = self.get_guild(guild_id)
        if not guild:
            return None
        for channel in guild.channels:
            if channel.id == channel_id:
                return channel
        return None

    def get_member(self, member_id: int, guild_id: int) -> Member:
        r"""Returns a :class:`Member` object if the user is found, else :class:`None`

        Returns
        -------
        :class:`Member`
            The member object that you searched for.
        """
        guild = self.get_guild(guild_id)
        return guild.get_member(member_id)

    def get_guild(self, guild_id: int) -> Guild:
        r"""Returns a :class:`Guild` object if the guild exists, else :class:`None` . There is almost no way, that this misses an existing guild.
        """
        for guild in self.guilds:
            if guild.id == guild_id:
                return guild

    async def fetch_channel(self, channel_id: int) -> Union[Channel, TextChannel]:
        r"""Returns a channel with a provided id.
        This is an API request. Use :meth:`Client.get_channel` to get a channel from the cache.
        """
        return await self.http.fetch_channel(channel_id)

    async def change_presence(self, status = None, activity: Activity = None, since = None):
        await self.http.ws.change_presence(status = status, activity = activity, since = since)
