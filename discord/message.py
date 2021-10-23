import aiohttp

base_url = "https://discord.com/api/v9"

class Message:
    def __init__(self, message_id: int = None, content: str = None, channel_id:int = None, author_id: str = None):
        self.message_id = message_id
        self.channel_id = channel_id
        self._author.id = author_id
        self.content: dict = {"content": f"{content}"}

    @property
    def get_message(self):
        return self.content