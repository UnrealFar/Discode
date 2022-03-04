
__all__ = ("Role",)

from typing import (
    TYPE_CHECKING,
)

from .abc import Snowflake
from ..flags import Permissions

class Role(Snowflake):
    r"""Represents a Discord role.__all__

    
    """

    if TYPE_CHECKING:
        id: int
        name: str
        colour: int
        hoist: bool
        position: int
        permissions: Permissions

    def __init__(self, connection, payload):
        self._connection = connection
        self.id = int(payload.pop("id"))
        self.name = payload.pop("name", None)
        self.colour = payload.pop("color", 0)
        self.hoist = payload.pop("hoist", False)
        self.position = payload.pop("position", None)
        self.permissions = Permissions(payload.pop("permissions", 0))

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"
