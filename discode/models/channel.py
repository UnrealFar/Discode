
from typing import (
    Any,
    Optional,
    List,
    Dict,
    overload
)

from .abc import MessageChannel

class TextChannel(MessageChannel):

    __slots__ = (
        "id",
        "name",
        "guild_id",
        "_connection"
    )

    def __init__(
        self,
        connection,
        payload: Dict[str, Any]
    ):
        self._connection = connection
        self.id: int = int(payload.pop("id"))
        connection.channel_cache[self.id] = self
        self.name: str = payload.pop("name", None)
        self.guild_id: int = payload.pop("guild_id", None)

    async def send(
        self,
        content: Optional[str] = ...,
        *,
        embeds: List = ...
    ):
        http = self._connection.http

        return await http.send_message(
            self.id,
            content = content,
            embeds = embeds
        )
