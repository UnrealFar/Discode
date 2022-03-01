import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .guild import Guild
    from .channel import DMChannel

from .user import User
from .abc import Snowflake
from ..utils import UNDEFINED

__all__ = ("Member",)

class Member(User):

    __slots__ = (
        "id",
        "_user",
        "name",
        "discriminator",
        "nick",
        "guild_id",
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
        self.guild_id = payload.pop("guild_id", None)
        user = payload.pop("user", {})
        uid = user.get("id")
        self._user: User = connection.get_user(uid)
        if not self._user:
            self._user: User = User(connection, user)
            connection.add_user(self._user)
        self.id: int = self._user.id
        self.name: str = self._user.name
        self.discriminator: str = self._user.discriminator
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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id = {self.id} name = {self.name} discriminator = {self.discriminator} nick = {self.nick}>"

    def __str__(self) -> str:
        return f"{self.display_name}#{self.discriminator}"

    @property
    def display_name(self) -> str:
        r""":class:`str`: Returns the nickname of the member if they have one, else their username"""
        return self.nick or self.name

    @property
    def guild(self):
        r""":class:`Guild`: The guild to which the member is attached to."""
        return self._connection.get_guild(self.guild_id)

    async def edit(
        self,
        *,
        nick: Optional[str] = UNDEFINED,
        mute: bool = UNDEFINED,
        deafen: bool = UNDEFINED,
        roles: List[Snowflake] = [],
        reason: Optional[str] = UNDEFINED
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
