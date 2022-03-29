from __future__ import annotations

from typing import (
    Any,
    Dict,
    Tuple,
    TYPE_CHECKING,
    Union,
)

if TYPE_CHECKING:
    from ..connection import Connection

from ..utils import UNDEFINED

class Interaction:

    __slots__: Tuple[str] = (
        "id",
        "type",
        "data",
        "guild_id",
        "channel_id",
        "application_id",
        "user",
        "message",
    )

    def __init__(self, connection: Connection, payload: Dict[str, Any]):
        self._connection: Connection = connection
        

