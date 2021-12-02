import asyncio

__all__ = ("TextChannel",)


class Channel:
    r"""Represents the base for a Discord channel.
    This can be a :class:`TextChannel`, a Category, a VoiceChannel, or a Thread.
    """

    def __init__(self, **data):
        self.data: dict = data
        self.http = data.get("http")
        self.loop = self.http.loop
        self.topic = data.get("topic")
        self.permissions = data.get("permission_overwrites")
        self.position = data.get("position")

    @property
    def name(self) -> str:
        return self.data.get("name", None)

    @property
    def id(self) -> int:
        return int(self.data.get("id"))

    @property
    def mention(self) -> str:
        return f"<#{self.id}>"

    @property
    def is_nsfw(self) -> bool:
        return self.data.get("nsfw", False) # haha nsfw go brrrr

class TextChannel(Channel):
    r"""Represents a Discord text channel.
    A text channel is a normal channel inside of a guild in which users can chat.
    """

    def __init__(self, **data):
        super().__init__(**data)
        self.type = 0

    @property
    def guild(self):
        r"""Get the guild that the text channel belongs to.
        """
        return self.http.client.get_guild(int(self.data.get("guild_id")))

    async def send(self, content = None, **kwargs):
        r"""Send a message to the text channel. Returns the sent :class:`Message`.
        """
        if content:
            kwargs["content"] = content

        message = await self.http.send_message(
            channel_id = self.id,
            **kwargs,
        )

        return message
