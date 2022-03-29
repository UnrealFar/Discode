from typing import Dict

from .models import Guild, Message, User
from .app import Button


class Connection:
    def __init__(self, client):
        self.me_id: int = None
        self.client = client
        self.http = client._http
        self.user_cache: Dict[int, User] = {}
        self.guild_cache: Dict[int, Guild] = {}
        self.message_cache: Dict[int, Message] = {}
        self.channel_cache = {}
        self.active_components: Dict[str, Button] = {}

    def get_user(self, user_id) -> User:
        return self.user_cache.get(user_id)

    def add_user(self, user: User) -> User:
        self.user_cache[user.id] = user
        return user

    def remove_user(self, user_id) -> User:
        return self.user_cache.pop(int(user_id), None)

    def get_guild(self, guild_id: int) -> Guild:
        return self.guild_cache.get(guild_id)

    def add_guild(self, guild: Guild) -> Guild:
        self.guild_cache[guild.id] = guild
        return guild

    def remove_guild(self, guild_id: int) -> Guild:
        return self.guild_cache.pop(guild_id, None)
