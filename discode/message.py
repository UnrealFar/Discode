import asyncio
from typing import Union, List

from .user import User
from .channel import TextChannel, DMChannel
from .embeds import Embed
from .member import Member
from .guild import Guild
from .components import Button, ActionRow

__all__ = ("Message",)


class Message:
    __slots__ = [
        "id",
        "content",
        "_author",
        "_member",
        "_channel",
        "author_id",
        "channel_id",
        "guild_id",
        "created_at",
        "edited_at",
        "http",
        "data"
    ]

    r"""
    Represents a Discord message.
    """

    def __init__(self, **data):
        self.data = data.copy()
        self.http = data.pop("http", None)

        self.id = int(data.pop("id", int()))
        self.content: str = data.pop("content", None)
        self._author: dict = data.pop("author", {})
        self.author_id: int = int(self._author.get("id", None))
        self.channel_id: int = int(data.pop("channel_id", None))
        self.guild_id: int = int(data.pop("guild_id", int()))
        self.created_at = data.pop("timestamp", None)
        self.edited_at = data.pop("edited_timestamp", None)

    @property
    def author(self) -> Union[User, Member]:
        r"""The person who created the message. Returns a :class:`Member` if the message was sent in a guild. If it wasn't, for example a DM, it returns a :class:`User` object.

        Returns
        --------
        Union[:class:`User`, :class:`Member`]
            The user or member who created the object.
        """
        if self.guild:
            if hasattr(self, "_member"):
                return self._member
            else:
                self._member = self.guild.get_member(self.author_id)
                return self._member
        else:
            return User(**self._author)

    @property
    def guild(self) -> Guild:
        """Returns the guild to which the message belongs to. If the guild doesn't exist, it returns :class:`None`

        Returns
        --------
        :class:`Guild`
            The Discord server to which the message belongs.
        """
        return self.http.client.get_guild(self.guild_id)
   
    @property
    def channel(self):
        return self._get_channel()

    @property
    def components(self) -> List[Button]:
        _c = self.data.get("components")
        ret = []
        for comp in _c:
            if comp.get("type") == 1:
                ret.append(ActionRow.from_json(comp))
            elif comp.get("type") == 2:
                ret.append(Button.from_json(comp))
        
        return ret

    @property
    def embeds(self) -> List[Embed]:
        ret = []
        _e = self.data.get("embeds", [])
        if self.data.get("embed"):
            _e.append(self.data["embed"])

        for emb in _e:
            ret.append(Embed.from_json(_e))

        return ret

    async def delete(self, reason: str = None) -> "Message":
        kwargs = {
            "method": "DELETE",
            "endpoint": f"/channels/{self.channel_id}/messages/{self.id}",
            "headers": {}
        }
        if reason:
            kwargs["headers"]["X-Audit-Log-Reason"] = reason

        await self.http.request(**kwargs)
        return self

    def _get_channel(self):
        if hasattr(self, "_channel"):
            return self._channel
        elif self.guild:
            self._channel = self.guild.get_channel(self.channel_id)
            return self._channel
        else:
            if isinstance(self.author, User):
                ch = getattr(self.author, "channel", None)
                if not ch:
                    ch = DMChannel(
                        id = self.channel_id,
                        http = self.http,
                        user = self.author
                    )
                    self._channel = ch
                    self._author._channel = ch
                return ch
            elif isinstance(self.author, Member):
                ch = getattr(self.author.user, "channel", None)
                if not ch:
                    ch = DMChannel(
                        id = self.channel_id,
                        http = self.http,
                        user = self.author.user
                    )
                    self._channel = ch
                    self.author.user._channel = ch
                return ch
