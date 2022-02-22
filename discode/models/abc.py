
from __future__ import annotations

import datetime
from typing import (
    List,
    Optional,
    Union,
    overload
)

class Snowflake:
    __slots__ = ()

    id: int


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
    channel: MessageChannel
    author: Union[User, GuildMember]


class Guild(Snowflake):

    name: str
    description: str
    icon: Asset
    banner: Asset


class MessageChannel(Snowflake):

    name: str

    async def send(
        self,
        content: Optional[str] = ...,
        *,
        embeds: List = ...
    ) -> BaseMessage:
        http = self._connection.http

        return await http.send_message(
            self.id,
            content = content,
            embeds = embeds
        )

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
