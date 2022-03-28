from __future__ import annotations

__all__ = ("Role",)

from typing import TYPE_CHECKING, Optional, Any

from ..flags import Permissions
from ..utils import UNDEFINED
from .abc import Snowflake


if TYPE_CHECKING:
    from .guild import Guild

class RoleTags:
    bot_id: Optional[int]
    integration_id: Optional[int]
    
    def __init__(self, **data):
        bot_id = int(data['bot_id']) if 'bot_id' in data else None
        integration_id = int(data['integration_id']) if 'integration_id' in data else None
        

        self.bot_id = bot_id
        self.integration_id = integration_id
        self._premium_subscriber = data.pop("premium_subscriber", UNDEFINED)

    def is_bot_role(self) -> bool:
        return self.bot_id is not None

    def is_premium_subscriber(self) -> bool:
        return self._premium_subscriber is None

class Role(Snowflake):
    r"""Represents a Discord role."""

    if TYPE_CHECKING:
        id: int
        name: str
        guild: Guild
        colour: int
        hoist: bool
        position: int
        permissions: Permissions
        tags: RoleTags

    def __init__(self, connection, payload):
        self._connection = connection
        self.id = int(payload.pop("id", UNDEFINED))
        self.name = payload.pop("name", None)
        self.guild = payload.pop("guild")
        self.colour = payload.pop("color", 0)
        self.hoist = payload.pop("hoist", False)
        self.position = payload.pop("position", None)
        self.permissions = Permissions(int(payload.pop("permissions", UNDEFINED)))
        self.tags = RoleTags(**payload.pop("tags", {}))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Role):
            return False
        if self.guild.id != other.guild.id:
            return False
        if self.id == other.id:
            return True

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Role):
            return False
        return self.is_lower_than(other)

    def __le__(self, other: Any) -> bool:
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Role):
            return False
        return self.is_greater_than(other)

    def __ge__(self, other: Any) -> bool:
        return self.__eq__(other) or self.__gt__(other)

    @property
    def mention(self) -> str:
        return f"<@&{self.id}>"

    def is_lower_than(self, other: Role) -> bool:
        if not isinstance(other, Role):
            fmt = f"Cannot compare object of type {other.__class__.__name__} with a Role object."
            raise TypeError(fmt)
        guild_id = self.guild.id
        if guild_id != other.guild.id:
            raise RuntimeError("Cannot compare roles from two different guilds.")

        if self.id == guild_id:
            return other.id != guild_id

        if self.position < other.position:
            return True

        if self.position == other.position:
            return self.id > other.id

        return False

    def is_greater_than(self, other: Role) -> bool:
        return not self.is_lower_than(other)
