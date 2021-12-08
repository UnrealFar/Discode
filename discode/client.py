import asyncio
import traceback
import sys
from typing import Optional, Callable, List, Union

from ._http import HTTP
from .user import ClientUser
from .guild import Guild
from .channel import Channel, TextChannel
from .member import Member
from .intents import Intents

__all__ = ("Client",)


class Client:
    r"""Represents the client that connects to the Discord API and the Gateway

    Parameters
    ----------
    message_limit: :class:`int`
        The maximum amount of messages to have in the cache. Messages are cached to reduce api callsand prevent ratelimits.

    chunk_at_startup: :class:`bool`
        If the client should chunk up all the guild members on startup. Defaults to :class:`True`.

    Attributes
    -----------
    loop: :class:`asyncio.AbstractEventLoop`
        The :class:`asyncio.AbstractEventLoop` to be used for asynchronous functions.
    """

    def __init__(self, **kwargs):
        self.loop: asyncio.AbstractEventLoop = kwargs.get("loop", asyncio.get_event_loop())
        self.__events: dict = {}
        self.message_cache = {}
        self.guilds: List[Guild] = {}
        self.chunk_guilds_at_startup: bool = True
        self.message_limit: int = kwargs.get("message_limit")
        self.intents = kwargs.get("intents", Intents.default())

    @property
    def user(self) -> ClientUser:
        r"""Returns the :class:`ClientUser` connected to the Discord Gateway.
        """
        return self.__user
    
    @property
    def is_ready(self):
        return self.http.ws._ready.is_set()

    @property
    def latency(self) -> float:
        try:
            return self.http.ws.get_latency()
        except Exception:
            return None
    
    

    async def dispatch(self, event: str, *args, **kwargs):
        if not self.is_ready and event != "ready":
            return

        _event = self.__events.get(event, None)
        if _event is not None:
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
        print(f"An error occured in {event}", file = sys.stderr)
        traceback.print_exception(
            type(exception),
            exception,
            exception.__traceback__,
            file = sys.stderr
        )

    def on_event(self, name: str):
        def decorator(func: Callable):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("Event must be a coroutine!")

            self.__events[name] = func

        return decorator

    async def start_task(self, token: str):
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

    def get_channel(self, channel_id: int, guild_id: int) -> Union[Channel, TextChannel, None]:
        guild = self.guilds.get(guild_id)
        for channel in guild.channels:
            if channel.id == channel_id:
                return channel
        return None

    def get_member(self, member_id: int, guild_id: int) -> Member:
        guild = self.guilds.get(guild_id)
        for member in guild.members:
            if member.id == member_id:
                return member
        return None

    def get_guild(self, guild_id: int) -> Guild:
        return self.http.ws.guilds.get(guild_id)

