from typing import Any, Dict, List

from .abc import Guild as _Guild
from .assets import Asset
from .member import Member


class Guild(_Guild):
    r"""Represents a Discord Guild."""

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
            m["guild"] = self
            mem = Member(connection, m)
            self._add_member(mem)
        self._channels: Dict = {}
        self._roles: Dict = {}

    @property
    def me(self) -> Member:
        return self.get_member(self._connection.my_id)

    @property
    def members(self) -> List[Member]:
        return [m for m in getattr(self, "_members", {}).values()]

    def get_member(self, member_id) -> Member:
        return self._members.get(int(member_id))

    def _add_member(self, member: Member) -> Member:
        self._members[member.id] = member
        return member

    def _remove_member(self, member: Member) -> Member:
        return self._members.pop(member.id, None)

    @property
    def channels(self):
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
