
from __future__ import annotations

from typing import (
    Any,
    Optional,
    List,
    Dict,
    TYPE_CHECKING,
    overload
)

if TYPE_CHECKING:
    from .message import Message
    from .guild import Guild
    from .user import User

from .abc import Snowflake

__all__ = (
    "TextChannel",
    "DMChannel"
)

class Messageable(Snowflake):

    async def send(
        self,
        content: Optional[str] = ...,
        *,
        embeds: List = [],
        files: List = []
    ) -> Message:
        r"""
        Send a message to the current channel.

        Parameters
        -----------
        content: Optional[:class:`str`]
            The content of the message to send.
        embeds: List[:class:`~discode.Embed`]
            A list containing embed objects.
        files: List[:class:`~discode.File`]

        Returns
        --------
        :class:`Message`
            The message that was sent to the destination.
        """
        http = self._connection.http

        return await http.send_message(
            self.id,
            content = content,
            embeds = embeds,
            files = files
        )

class TextChannel(Messageable):
    r"""
    Represents a text channel within a guild.

    Attributes
    -----------

    id: :class:`int`
        The unique ID of the channel.
    name: :class:`str`
        The name of the channel.
    type: :class:`int`
        The type of the channel. Returns 0.
    guild_id: :class:`int`
        The ID of the guild to which the channel belongs to.
    is_nsfw: :class:`bool`
        Returns whether the channel is an NSFW channel.
    """

    __slots__ = (
        "id",
        "name",
        "type",
        "guild_id",
        "is_nsfw",
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
        self.type: int = 0
        guild_id = payload.pop("guild_id", None)
        self.guild_id = int(guild_id) if guild_id else None
        self.is_nsfw: bool = payload.pop("nsfw", False)

    @property
    def guild(self) -> Guild:
        r""":class:`Guild`: The guild to which the channel belongs to."""
        return self._connection.get_guild(self.guild_id)

class DMChannel(Messageable):

    __slots__ = (
        "id",
        "type",
        "recepients"
        "_connection"
    )

    def __init__(self, connection, payload):
        self._connection = connection
        self.id = int(payload.pop("id"))
        self.recepients: List[User] = []
        for recep in payload.pop("recepients", []):
            rec = connection.get_user(recep.get("id"))
            self.recepients.append(rec)
        self.type = 1
