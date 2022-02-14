from __future__ import annotations

import datetime
from typing import List, Optional


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


class Guild(Snowflake):

    name: str
    description: str
    icon: Asset
    banner: Asset


class GuildMember(Snowflake):

    user: User
    name: str
    id: int
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
