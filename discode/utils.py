from typing import Any, Iterable, final


@final
class _UNDEFINED:
    def __repr__(self) -> str:
        return "..."

    __str__ = __repr__

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)

    def __bool__(self) -> bool:
        return False


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
    return ret
