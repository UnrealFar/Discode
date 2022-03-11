from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, List, Optional, Union, overload

if TYPE_CHECKING:
    from ..connection import Connection
    from ..utils import UNDEFINED

__all__ = (
    "Snowflake",
)


class Snowflake:
    __slots__ = tuple()

    id: int
    if TYPE_CHECKING:
        _connection: Connection

    def __init__(self, connection: Connection, payload: dict):
        self.id = payload.pop(id, UNDEFINED)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id = {self.id}>"

    def _copy(self, **kwargs):
        ret = self.__class__(self._connection, {"id": self.id})
        for slot in self.__slots__:
            if hasattr(self, slot):
                setattr(ret, slot, getattr(self, slot))

