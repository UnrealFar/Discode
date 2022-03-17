from __future__ import annotations

import asyncio
import functools
from typing import TYPE_CHECKING, Any, Callable, Iterable, Union, final

if TYPE_CHECKING:
    from .flags import Permissions


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
    permissions: Union[Permissions, int] = UNDEFINED,
    scopes: Iterable[str] = UNDEFINED,
    redirect_uri: str = UNDEFINED,
) -> str:
    r"""Generates an invite url based on the given parameters for the client.

    Returns
    -------
    :class:`str`
        The invite url generated.
    """
    ret = f"https://discord.com/oauth2/authorize?client_id={client_id}"
    ret += "&scope=" + "+".join(scopes or ("bot","application.commands"))
    if permissions:
        ret += f"&permissions={int(permissions)}"
    return ret


def get_event_loop() -> asyncio.AbstractEventLoop:
    r"""Alternative to :meth:`asyncio.get_event_loop`.
    Creates a new loop or fetches an existing event loop and returns it.
    Avoids :class:`DeprecationWarning` warning to be thrown while called in Python v3.10 and higher versions.

    Returns
    -------
    :class:`asyncio.AbstractEventLoop`
        The existing or newly created loop.
    """
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.new_event_loop()


def async_function(sync_function: Callable):
    r"""Decorator to make synchronous function asynchronous. Useful with modules like Pillow, which have a synchronous backend but are extremely useful in image manipulation.

    Usage of this decorator is equivalant to:

    .. code-block:: py

        # inside coroutine:
        await get_event_loop().run_in_executor(
            None,
            functools.partial(sync_function, *args, **kwargs)
        )

    Example
    --------

    .. code-block:: py

        @discode.utils.async_function
        def sync_function(msg: discode.Message):
            do_synchronous_operations_with_message(msg)


        @client.on_event("message_create")
        async def on_message(msg):
            await sync_function(msg)

    """

    @functools.wraps(sync_function)
    async def wrapper(*args, **kwargs):
        r"""Internal wrapper to run code asynchronously."""
        partial = functools.partial(sync_function, *args, **kwargs)
        loop = get_event_loop()
        return loop.run_in_executor(None, partial)

    return wrapper


@async_function
def run_async(func, *args, **kwargs):
    r"""Run a function asynchronously and wait for it to complete.

    Returns
    -------

    Any
        The return value of the function.
    """
    return func(*args, **kwargs)


def escape_markdown(text: str):
    r"""Get rid of Discord markdown highlighting from given text.

    Parameters
    ----------

    text: :class:`str`
        The text to get freed from markdown highlighting in Discord.

    Returns
    -------

    :class:`str`
        Text passed in text parameter freed from Discord markdown highlighting.
    """
    return (
        text.replace("*", "\*")
        .replace("_", "\_")
        .replace("`", "\`")
        .replace("|", "\|")
        .replace("~", "\~")
        .replace(">", "\>")
    )
