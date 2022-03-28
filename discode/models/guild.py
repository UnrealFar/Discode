from typing import Any, Dict, List, Optional, Union

from ..utils import UNDEFINED
from .abc import Snowflake
from .assets import Asset
from .channel import TextChannel
from .member import Member
from .role import Role
from .emoji import Emoji

__all__ = ("Guild",)


class Guild(Snowflake):
    r"""
    Represents a Discord Guild.

    Attributes
    ----------

    id: :class:`int`
        The unique ID of the guild.
    name: :class:`str`
        The name of the guild.
    """

    __slots__ = (
        "id",
        "name",
        "owner_id",
        "_members",
        "_channels",
        "_roles",
        "_icon",
        "_emojis",
        "_connection",
    )

    def __init__(self, connection, payload: Dict[str, Any]):
        self._connection = connection
        self.id: int = int(payload.pop("id", UNDEFINED))
        self.name: str = payload.pop("name", None)
        self.owner_id: int = int(payload.pop("owner_id", UNDEFINED))
        self._icon: str = payload.pop("icon", None)
        self._channels: Dict[int, TextChannel] = {}
        for c in payload.pop("channels", tuple()):
            c["guild"] = self
            if c["type"] == 0:
                ch = TextChannel(connection, c)
                self._add_channel(ch)
        self._roles: Dict[int, Role] = {}
        for r in payload.pop("roles", tuple()):
            r["guild"] = self
            role = Role(connection, r)
            self._add_role(role)
        self._emojis: Dict[int, Emoji] = {}
        self._members: Dict[int, Member] = {}
        for m in payload.pop("members", tuple()):
            m["guild"] = self
            mem = Member(connection, m)
            self._add_member(mem)
        for e in payload.pop("emojis", ()):
            emoji = Emoji(connection, e)
            self._emojis[emoji.id] = emoji

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} name={self.name}>"

    @property
    def me(self) -> Member:
        r""":class:`Member`: The member object of the client user in the guild."""
        return self.get_member(self._connection.me_id)

    @property
    def members(self) -> List[Member]:
        r"""List[:class:`Member`]: An arry of all the members in the guild."""
        return list(self._members.values())

    def get_member(self, member_id) -> Member:
        r"""
        Get a :class:`Member` from the cache who matches the member_id parameter.

        Returns
        -------
        :class:`Member`
            The member that was retrieved from the cache
        """
        return self._members.get(int(member_id))

    def _add_member(self, member: Member) -> Member:
        self._members[member.id] = member
        return member

    def _remove_member(self, member: Member) -> Member:
        return self._members.pop(member.id, None)

    @property
    def channels(self) -> Union[TextChannel]:
        r"""List[:class:`TextChannel`]: All the channels attached to the guilds cached by the client."""
        return list(self._channels.values())

    @property
    def text_channels(self) -> List[TextChannel]:
        r"""List[:class:`TextChannel`]: All the text channels cached by the guild."""
        return [c for c in self._channels.values() if c.type == 0]

    def _add_channel(self, channel):
        self._channels[channel.id] = channel

    def _remove_channel(self, channel):
        self._channels.pop(channel.id, None)

    @property
    def roles(self) -> List[Role]:
        return list(self._roles.values())

    @property
    def default_role(self) -> Role:
        return self.get_role(self.id)

    @property
    def me_role(self) -> Role:
        me_id = self._connection.me_id
        for r in self._roles.values():
            if r.tags.bot_id == me_id:
                return r

    def get_role(self, role_id: int) -> Optional[Role]:
        return self._roles.get(role_id)

    def _add_role(self, role):
        self._roles[role.id] = role

    def _remove_role(self, role):
        self._roles.pop(role.id, None)

    @property
    def emojis(self) -> List[Emoji]:
        return list(self._emojis.values())

    @property
    def icon(self) -> Asset:
        return Asset.guild_icon(self)
