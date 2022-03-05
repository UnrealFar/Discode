
from __future__ import annotations

import asyncio
import functools

from typing import (
    Any,
    Iterable,
    Callable,
    final,
    TYPE_CHECKING,
)


@final
class _UNDEFINED:
    __slots__ = tuple()

    if TYPE_CHECKING:
        __repr__: Callable[str]
        __str__: Callable[str]
        __int__: Callable[int]
        __eq__: Callable[bool]
        __bool__: Callable[bool]

    __repr__ = lambda self: "..."

    __str__ = lambda self: "UNDEFINED"

    __int__ = lambda self: 0

    __eq__ = lambda self, other: isinstance(other, self.__class__)

    __bool__ = lambda self: False


UNDEFINED: Any = _UNDEFINED()


def invite_url(
    client_id,
    *,
    permissions: int = UNDEFINED,
    scopes: Iterable[str] = UNDEFINED,
    redirect_uri: str = UNDEFINED,
) -> str:
    r"""Generates an invite url based on the given parameters for the client.
    """
    ret = f"https://discord.com/oauth2/authorize?client_id={client_id}"
    ret += "&scope=" + "".join(scopes or ("bot",))
    if permissions:
        ret += f"&permissions={int(permissions)}"
    return ret


def async_function(sync_function: Callable):
    r"""Decorator to make synchronous function asynchronous. Useful with modules like Pillow, which have a synchronous backend but are extremely useful in image manipulation.

    Example
    --------

    .. codeblock:: python3

        @discode.utils.async_function
        def sync_function(msg: discode.Message):
            do_synchronous_operations_with_message(msg)


        @client.on_event("message_create")
        async def on_message(msg):
            await sync_function(msg)

    """

    @functools.wraps(sync_function)
    async def wrapper(*args, **kwargs):
        r"""Internal wrapper to run code asynchronously.
        """
        partial = functools.partial(sync_function, *args, **kwargs)
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, partial)
    return wrapper


def escape_markdown(text: str):
    r"""Get rid of Discord markdown from given text.
    """
    return text.replace("*", "\*").replace("_", "\_").replace("`", "\`").replace("|", "\|").replace("~", "\~").replace(">", "\>")


