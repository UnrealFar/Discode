import datetime
from typing import Any, Dict, List, Optional

from .abc import GuildMember, Snowflake
from .user import User


class Member(GuildMember):

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
        self._guild = payload.pop("guild")
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

    def __repr__(self) -> str:
        return f"<{self.__class__.name} id = {self.id} name = {self.name} discriminator = {self.discriminator} nick = {self.nick}>"

    def __str__(self) -> str:
        return f"{self.display_name}#{self.discriminator}"

    @property
    def display_name(self) -> str:
        return self.nick if self.nick else self.name

    async def edit(
        self,
        *,
        nick: Optional[str] = ...,
        mute: bool = ...,
        deafen: bool = ...,
        roles: List[Snowflake] = ...,
        reason: Optional[str] = ...,
    ):
        kwargs = dict()
        guild_id = self.guild.id
        http = self._connection.http
        if nick != ...:
            kwargs["nick"] = nick
        if deafen != ...:
            kwargs["mute"] = mute
        if deafen != ...:
            kwargs["deaf"] = deafen
        if roles != ...:
            kwargs["roles"] = tuple(str(r.id) for r in roles)
        if len(kwargs) >= 1:
            await http.edit_member(guild_id, self.id, kwargs, reason)
