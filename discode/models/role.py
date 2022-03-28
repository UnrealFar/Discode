from __future__ import annotations

__all__ = ("Role",)

from typing import TYPE_CHECKING, Optional

from ..flags import Permissions
from ..utils import UNDEFINED, NamedTuple
from .abc import Snowflake

class RoleTags(NamedTuple):
    bot_id: Optional[int]
    integration_id: Optional[int]
    premium_subscriber: bool
    
    def __init__(self, **data):
        bot_id = int(data['bot_id']) if 'bot_id' in data else None
        integration_id = int(data['integration_id']) if 'integration_id' in data else None
        
        super().__init(
            "RoleTags",
            **{
                "bot_id": bot_id,
                "integration_id": integration_id,
                "premium_subscriber": data.pop("premium_subscriber", False)
            }
        )

class Role(Snowflake):
    r"""Represents a Discord role."""

    if TYPE_CHECKING:
        id: int
        name: str
        colour: int
        hoist: bool
        position: int
        permissions: Permissions
        tags: RoleTags

    def __init__(self, connection, payload):
        self._connection = connection
        self.id = int(payload.pop("id", UNDEFINED))
        self.name = payload.pop("name", None)
        self.colour = payload.pop("color", 0)
        self.hoist = payload.pop("hoist", False)
        self.position = payload.pop("position", None)
        self.permissions = Permissions(int(payload.pop("permissions", UNDEFINED)))
        self.tags = RoleTags(**payload.pop("tags", {}))

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"
