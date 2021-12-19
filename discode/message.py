import asyncio
from typing import Union, List

from .user import User
from .channel import TextChannel, Channel
from .embeds import Embed
from .member import Member
from .guild import Guild
from .components import Button

__all__ = ("Message",)


class Message:
    r"""
    Represents a Discord message.
    """

    def __init__(self, **data):
        self.data = data
        self.http = data.get("http")
        self.loop = self.http.loop
        self.created_at = data.get("timestamp")
        self.mentions = data.get("mentions")
        self.id = int(data.get("id"))
        self.content = data.get("content")
        self.__author: dict = data.get("author")
        self.__member: dict = data.get("member")
        self.edited_at = data.get("edited_timestamp")

    @property
    def author(self) -> Union[User, Member]:
        r"""The person who created the message. Returns a :class:`Member` if the message was sent in a guild. If it wasn't, for example a DM, it returns a :class:`User` object.

        Returns
        --------
        Union[:class:`User`, :class:`Member`]
            The user or member who created the object.
        """
        data = self.__author
        data["http"] = self.http
        if self.guild:
            data = self.__member
            data["http"] = self.http
            data["user"] = self.__author
            return Member(**data)
        return User(**data)

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
    def guild_id(self) -> int:
        try:
            return int(self.data.get("guild_id"))
        except: return None

    @property
    def channel_id(self) -> int:
        try:
            return int(self.data.get("channel_id"))
        except: return None
    
    @property
    def channel(self):
        return self.http.client.get_channel(self.channel_id, self.guild_id)

    @property
    def components(self) -> List[Button]:
        _c = self.data.get("components")
        ret = []
        for comp in _c:
            if comp.get("type") == 2:
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
