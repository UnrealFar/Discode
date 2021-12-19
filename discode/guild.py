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
        if getattr(self, "_members", None):
            return self._members

    @property
    def channels(self) -> List[Union[TextChannel, Channel]]:
        if hasattr(self, "_channels"):
            return self._channels

        self._channels = []
        for ch in self.data.get("channels"):
            ch["http"] = self.http
            _type = ch.get("type")
            if _type == 0:
                self._channels.append(TextChannel(**ch))
            else:
                self._channels.append(Channel(**ch))

        return self._channels
