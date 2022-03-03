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
        __eq__: Callable[bool]
        __bool__: Callable[bool]

    __repr__ = lambda self: "..."

    __str__ = lambda self: "UNDEFINED"

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
    ret = f"https://discord.com/oauth2/authorize?client_id={client_id}"
    ret += "&scope=" + "".join(scopes or ("bot",))
    if permissions:
        ret += f"&permissions={int(permissions)}"
    return ret
