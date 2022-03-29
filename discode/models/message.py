from __future__ import annotations

__all__ = ("Message", "MessageReference")

from typing import Any, Optional, Dict, List, Union, TYPE_CHECKING

from ..app import Button, LinkButton, component_from_dict
from ..utils import UNDEFINED
from .abc import Snowflake
from .channel import TextChannel
from .guild import Guild
from .member import Member
from .user import User

if TYPE_CHECKING:
    from ..connection import Connection


class MessageReference(Snowflake):

    __slots__ = (
        "id",
        "channel_id",
        "guild_id",
        "fail_if_not_exists",
        "referrer",
        "_connection",
    )

    if TYPE_CHECKING:
        id: int
        _connection: Connection
        channel_id: Optional[int]
        guild_id: Optional[int]
        fail_if_not_exists: bool
        referrer: Message

    def __init__(self, connection, payload: Dict[str, Any]):
        self._connection = connection
        self.id = int(payload.pop("message_id", UNDEFINED))
        self.channel_id = int(payload.pop("channel_id", UNDEFINED))
        self.guild_id = int(payload.pop("guild_id", UNDEFINED))
        self.fail_if_not_exists = payload.pop("fail_if_not_exists", True)
        self.referrer = payload.pop("msg")

    @property
    def cached_message(self) -> Optional[Message]:
        return self._connection.message_cache.get(self.id)

    async def fetch_message(self) -> Optional[Message]:
        http = self._connection.http
        msg_payload = await http.request(
            "GET",
            "/channels/{channel_id}/messages/{message_id}",
            parameters={"channel_id": self.channel_id, "message_id": self.id},
        )
        return Message(self._connection, msg_payload)


class Message(Snowflake):

    __slots__ = (
        "id",
        "content",
        "channel_id",
        "guild_id",
        "author_id",
        "reference",
        "_components",
        "_mentions",
        "_connection",
    )

    if TYPE_CHECKING:
        id: int
        _connection: Connection
        content: str
        channel_id: int
        guild_id: Optional[int]
        author_id: int
        reference: MessageReference

    def __init__(self, connection, payload: Dict[str, Any]):
        self._connection = connection
        self.id = int(payload.pop("id"))
        self.content = payload.pop("content", None)
        self.channel_id = int(payload.pop("channel_id"))
        self.guild_id = int(payload.pop("guild_id", UNDEFINED))
        self.author_id = int(payload.pop("author", {}).get("id", 0))
        self._components = [
            component_from_dict(comp) for comp in payload.pop("components", ())
        ]
        ref = payload.pop("message_reference", UNDEFINED)
        if ref != UNDEFINED:
            ref["msg"] = self
            self.reference = MessageReference(connection, ref)
        else:
            self.reference = None
        ms_data = payload.pop("mentions", ())
        self._mentions = []
        if len(ms_data) >= 1:
            for md in ms_data:
                u = connection.get_user(int(md.get("id", UNDEFINED)))
                if u:
                    self._mentions.append(u)

    def copy(self, **options):
        payload = {"id": self.id, "channel_id": options['channel_id']}
        ret = Message(self._connection, payload)
        ret.content = options.get("content")
        ret.guild_id = ret.guild_id = self.guild_id
        ret.author_id = self.author_id
        if options.get("components") and len(options["components"] >= 1):
            ret._components = [component_from_dict(comp) for comp in options["components"]]
        ret.reference = self.reference
        ms_data = options.pop("mentions", ())
        if len(ms_data) >= 1:
            for md in ms_data:
                u = self._connection.get_user(int(md.get("id", UNDEFINED)))
                if u:
                    ret._mentions.append(u)
        return ret

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id = {self.id} content = {self.content}"

    def __str__(self) -> str:
        return self.content or ""

    @property
    def author(self) -> Union[User, Member]:
        g = self.guild
        if g:
            return g.get_member(self.author_id)
        return self._connection.get_user(self.author_id)

    @property
    def channel(self) -> TextChannel:
        return self._connection.channel_cache.get(self.channel_id)

    @property
    def guild(self) -> Guild:
        return self._connection.get_guild(self.guild_id)

    @property
    def components(self) -> List[Union[Button, LinkButton]]:
        return self._components.copy()

    @property
    def mentions(self) -> List[User]:
        return self._mentions.copy()
