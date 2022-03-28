from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from .guild import Guild
    from .channel import DMChannel

from ..utils import UNDEFINED
from ..flags import Permissions
from .abc import Snowflake
from .role import Role
from .user import User

__all__ = ("Member",)


class Member(User):

    if TYPE_CHECKING:
        id: int
        name: str
        discriminator: str

    __slots__ = (
        "id",
        "_user",
        "name",
        "discriminator",
        "nick",
        "_guild",
        "_roles",
        "joined_at",
        "dm_channel",
        "premium_since",
        "_avatar",
        "_banner",
        "_connection",
    )

    def __init__(self, connection, payload: Dict[str, Any]):
        self._connection = connection
        user = payload.pop("user", {})
        uid = user.get("id")
        self._user = connection.get_user(uid)
        if not self._user:
            self._user = User(connection, user)
            connection.add_user(self._user)
        self.id = self._user.id
        self.name = self._user.name
        self.discriminator = self._user.discriminator
        self.nick: str = payload.pop("nick", None)
        self.joined_at = None
        self.premium_since = None
        if payload.get("joined_at"):
            self.joined_at: datetime.datetime = datetime.datetime.fromisoformat(
                payload.pop("joined_at")
            )
        if payload.get("premium_since"):
            self.premium_since: datetime.datetime = datetime.datetime.fromisoformat(
                payload.pop("premium_since")
            )
        self._avatar: str = payload.pop("avatar", None)
        self._banner: str = payload.pop("banner", None)
        self.dm_channel: DMChannel = None
        guild = payload.pop("guild")
        self._guild: Guild = guild
        roles = {}
        self._roles: Dict[int, Role] = roles
        for r in payload.pop("roles", ()):
            role = guild.get_role(int(r))
            roles[role.id] = role

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id = {self.id} name = {self.name} discriminator = {self.discriminator} nick = {self.nick}>"

    def __str__(self) -> str:
        return f"{self.display_name}#{self.discriminator}"

    @property
    def display_name(self) -> str:
        r""":class:`str`: Returns the nickname of the member if they have one, else their username"""
        return self.nick or self.name

    @property
    def guild(self) -> Guild:
        r""":class:`Guild`: The guild to which the member is attached to."""
        return self._guild

    @property
    def roles(self) -> List[Role]:
        return list(self._roles.values())

    @property
    def user(self) -> User:
        return self._user

    @property
    def guild_permissions(self) -> Permissions:
        guild = self.guild
        if guild.owner_id == self.id:
            return Permissions.all()
        ret = Permissions(0)
        for r in self._roles.values():
            ret.value |= r.permissions.value
        if ret.administrator:
            return Permissions.all()
        return ret

    async def edit(
        self,
        *,
        nick: Optional[str] = UNDEFINED,
        mute: bool = UNDEFINED,
        deafen: bool = UNDEFINED,
        roles: List[Snowflake] = [],
        reason: Optional[str] = UNDEFINED,
    ):
        r"""
        Edit the member.

        Returns
        -------
        :class:`Member`
            The member which was edited.
        """
        kwargs = dict()
        http = self._connection.http
        if nick != UNDEFINED:
            nick = str(nick)
            kwargs["nick"] = nick
            self.nick = nick
        if deafen != UNDEFINED:
            kwargs["mute"] = mute
        if deafen != UNDEFINED:
            kwargs["deaf"] = deafen
        if len(roles) >= 1:
            kwargs["roles"] = tuple(str(r.id) for r in roles)
        if len(kwargs) >= 1:
            await http.edit_member(self, kwargs, reason)

        return self
