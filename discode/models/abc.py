from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, List, Optional, Union, overload

if TYPE_CHECKING:
    from ..connection import Connection

__all__ = (
    "Snowflake",
    "BaseMessage",
    "Guild",
    "Asset"
    )


class Snowflake:
    __slots__ = tuple()

    id: int
    if TYPE_CHECKING:
        _connection: Connection

    def __init__(self, connection: Connection, payload: dict):
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id = {self.id}>"


class BaseMessage(Snowflake):

    content: str
    channel_id: int


class Guild(Snowflake):

    name: str
    description: str
    icon: Asset
    banner: Asset


class Asset:

    BASE_URL = "https://cdn.discordapp.com"
    url: str
