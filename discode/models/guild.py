from typing import Any, Dict, List

from .abc import Guild as _Guild
from .assets import Asset
from .member import Member
from .channel import TextChannel

__all__ = (
    "Guild",
)

class Guild(_Guild):
    r"""
    Represents a Discord Guild.

    Attributes
    ----------

    id: :class:`int`
        The unique ID of the guild.
    name: :class:`str`
        The bane of the guild.
    """

    __slots__ = (
        "id",
        "name",
        "_members",
        "_channels",
        "_roles",
        "_icon",
        "_connection",
    )

    def __init__(self, connection, payload: Dict[str, Any]):
        self._connection = connection
        self.id: int = int(payload.pop("id"))
        self.name: str = payload.pop("name", None)
        self._icon: str = payload.pop("icon", None)
        self._members: Dict[int, Member] = {}
        for m in payload.pop("members", []):
            m["guild_id"] = self.id
            mem = Member(connection, m)
            self._add_member(mem)
        self._channels: Dict = {}
        for c in payload.pop("channels", []):
            c["guild"] = self
            if c["type"] == 0:
                ch = TextChannel(connection, c)
                self._add_channel(ch)
        self._roles: Dict = {}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id = {self.id} name = { self.name,}>"

    @property
    def me(self) -> Member:
        r""":class:`Member`: The member object of the client user in the guild."""
        return self.get_member(self._connection.my_id)

    @property
    def members(self) -> List[Member]:
        r"""List[:class:`Member`]: An arry of all the members in the guild."""
        return [m for m in getattr(self, "_members", {}).values()]

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
    def channels(self):
        r"""List[:class:`TextChannel`]: All the channels attached to the guild cached by the client."""
        return [c for c in getattr(self, "_roles", {}).values()]

    def _add_channel(self, channel):
        self._channels[channel.id] = channel

    def _remove_channel(self, channel):
        self._channels.pop(channel.id, None)

    @property
    def roles(self) -> List[Dict[str, Any]]:
        return [r for r in getattr(self, "_roles", {}).values()]

    def _add_role(self, role):
        self._roles[role.id] = role

    def _remove_role(self, role):
        self._roles.pop(role.id, None)

    @property
    def icon(self) -> Asset:
        return Asset.guild_icon(self)
