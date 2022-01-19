from typing import List, Union

from .channel import TextChannel, Channel
from .member import Member

class Guild:
    def __init__(self, **data):
        self.http = data.get("http")
        self.loop = self.http.loop
        self.data = data
        self.id = int(data.get("id"))
        self.name = data.get("name")
        self.icon = data.get("icon")
        self.splash = data.get("splash")
        self.discovery_splash: data.get("discovery_splash")
        self.emojis = data.get("emojis")
        self.description = data.get("description")
        self.owner_id = int(data.get("owner_id"))
        self.region = data.get("region")
        self.afk_channel_id = data.get("afk_channel_id")
        self.afk_timeout = data.get("afk_timeout")
        self.default_message_notifications = data.get("default_message_notifications")
        self.explicit_content_filter = data.get("explicit_content_filter")
        self.roles = data.get("roles")
        self.rules_channel_id = data.get("rules_channel_id")
        self.vanity_url_code = data.get("vanity_url_code")
        self.banner = data.get("banner")
        self.premium_tier = data.get("premium_tier")
        self._members: dict = {}
        self._channels: dict = data.get("_channels")

    @property
    def mfa_level(self) -> int:
        return self.data.get("mfa_level")

    @property
    def verification_level(self) -> int:
        return self.data.get("verification_level")

    @property
    def nsfw_level(self) -> int:
        return self.data.get("nsfw_level")

    @property
    def features(self) -> list:
        data_features = self.data.get("features")
        if not data_features:
            return data_features
        else:
            new_features = []
            for feature in data_features:
                new_features.append(feature.lower())
            return new_features

    @property
    def members(self) -> List[Member]:
        memlist = []
        if getattr(self, "_members", None):
            for mem in self._members:
                memlist.append(self._members[mem])
        return memlist

    @property
    def channels(self) -> List[Union[TextChannel, Channel]]:
        return [self._channels[ch_id] for ch_id in self._channels]

    def get_member(self, member_id):
        return self._members.get(member_id)

    def get_channel(self, channel_id: int) -> Union[Channel, TextChannel]:
        return self._channels.get(channel_id)
