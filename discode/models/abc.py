
from __future__ import annotations

import datetime
from typing import (
    List,
    Optional,
    Union,
    TYPE_CHECKING,
    overload
)

if TYPE_CHECKING:
    from ..connection import Connection

__all__ = (
    "Snowflake",
    "User",
    "BaseMessage",
    "Guild",
    "GuildMember",
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

class User(Snowflake):

    name: str
    discriminator: str
    bot: bool
    avatar: Asset
    banner: Asset

    @property
    def display_name(self) -> str:
        raise NotImplementedError

class BaseMessage(Snowflake):

    content: str
    channel_id: int
    author: Union[User, GuildMember]


class Guild(Snowflake):

    name: str
    description: str
    icon: Asset
    banner: Asset

class GuildMember(User):

    user: User
    guild: Guild
    name: str
    discriminator: str
    bot: bool
    system: bool
    created_at: datetime.datetime
    default_avatar: Asset
    avatar: Optional[Asset]
    mutual_guilds: List[Guild]
    banner: Optional[Asset]

class Asset:

    BASE_URL = "https://cdn.discordapp.com"
    url: str
