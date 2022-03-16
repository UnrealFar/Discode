from __future__ import annotations

__all__ = ("Emoji",)

from typing import Any, Optional, List, Dict, TYPE_CHECKING

from .abc import Snowflake
from .role import Role
from .user import User
from ..utils import UNDEFINED

if TYPE_CHECKING:
    from ..connection import Connection

class Emoji(Snowflake):

    if TYPE_CHECKING:
        id: Optional[int]
        name: Optional[str]
        roles: List[Optional[Role]]
        user: Optional[User]
        require_colons: Optional[bool]
        managed: Optional[bool]
        available: bool
        animated: bool
        _connection: Connection

    def __init__(self, connection, payload: Dict[str, Any]):
        self._connection = connection
        _id = int(payload.pop("id", UNDEFINED))
        self.id = _id if id != 0 else None
        self.name = payload.pop("name", None)
        self.roles = []
        rs = payload.pop("roles", ())
        for r in rs:
            self.roles.append(Role(connection, r))
        _user = payload.pop("user", None)
        user = None
        if isinstance(_user, dict):
            user = self._connection.get_user(int(_user.get("id", UNDEFINED)))
            if not user:
                user = User(connection, _user)
        self.user = user
        self.require_colons = payload.pop("require_colons", True)
        self.managed = payload.pop("managed", False)
        self.available = payload.pop("available", True)
        self.animated = payload.pop("animated", True)

    def __repr__(self) -> str:
        return f"<Emoji id={self.id} name={self.name}>"

    def __str__(self) -> str:
        return f"<:{self.name}:{self.id}>" if self.id else f":{self.name}:"
