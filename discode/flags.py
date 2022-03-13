from __future__ import annotations

from typing import Any, Dict, Iterator, Optional, Tuple, Type, Union

__all__ = ("Intents",)


class Flags:

    __items__: Dict[str, int]
    __settings__: Dict[str, Any]

    def __init__(self, value: int = 0, **flags):
        self.value: int = value
        for flag, toggle in flags.items():
            if flag not in self.__items__:
                raise TypeError(f"{flag} is not a valid flag for {self.__class__.__name__}")
            self._apply(flag, toggle)

    def _apply(self, flag: str, toggle: bool):
        value = self.__items__[flag]

        if toggle is True:
            self.value |= value
        elif toggle is False:
            self.value &= ~value
        else:
            raise TypeError(f"{flag} must be a bool, not {toggle.__class__!r}")

    def __init_subclass__(cls):
        items = dict()

        for k, v in vars(cls).items():
            if (k.startswith("_")) or (not isinstance(v, int)):
                continue
            else:
                items[k] = v
                setattr(cls, k, Flag(k, v))

        cls.__items__ = items

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} value={self.value}>"

    def __int__(self) -> int:
        return self.value

    def __iter__(self) -> Iterator[Tuple[str, bool]]:
        for n in self.__items__:
            yield getattr(self, n)

    __eq__ = (
        lambda self, other: isinstance(other, self.__class__)
        and self.value == other.value
    )
    __ne__ = (
        lambda self, other: isinstance(other, self.__class__)
        and self.value != other.value
    )
    __lt__ = (
        lambda self, other: isinstance(other, self.__class__)
        and self.value < other.value
    )
    __le__ = (
        lambda self, other: isinstance(other, self.__class__)
        and self.value <= other.value
    )
    __gt__ = (
        lambda self, other: isinstance(other, self.__class__)
        and self.value > other.value
    )
    __ge__ = (
        lambda self, other: isinstance(other, self.__class__)
        and self.value >= other.value
    )


class Flag:
    __slots__ = ("name", "value")

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def __get__(
        self, instance: Optional[Flags], owner: Type[Flags]
    ) -> Union[int, bool]:
        if instance is None:
            return self.value

        return instance.value & self.value > 0

    def __set__(self, instance: Optional[Flags], toggle: bool) -> None:
        if instance is None:
            raise AttributeError(
                "Cannot set this attribute on non-instansiated Flags class."
            )

        instance.apply(self.name, toggle)


class Intents(Flags):
    guilds = 1 << 0
    members = 1 << 1
    bans = 1 << 2
    emojis_and_stickers = 1 << 3
    integrations = 1 << 4
    webhooks = 1 << 5
    invites = 1 << 6
    voice_states = 1 << 7
    presences = 1 << 8
    guild_messages = 1 << 9
    guild_reactions = 1 << 10
    guild_typing = 1 << 11
    direct_messages = 1 << 12
    direct_messages_reactions = 1 << 13
    direct_messages_typing = 1 << 
    message_content = 1 << 15
    guild_scheduled_events = 1 << 16


    @classmethod
    def all(cls) -> Intents:
        return cls(**{k: True for k in cls.__items__})

    @classmethod
    def unprivileged(cls) -> Intents:
        ret = cls.all()
        ret.members = False
        ret.presences = False
        ret.guild_messages = False
        return ret

    @classmethod
    def default(cls) -> Intents:
        ret = cls.unprivileged()
        ret.guild_messages = True
        return ret

class Permissions(Flags):
    create_instant_invite = 1 << 0
    kick_members = 1 << 1
    ban_members = 1 << 2
    administrator = 1 << 3
    manage_channels = 1 << 4
    manage_guild = 1 << 5
    add_reactions = 1 << 6
    view_audit_log = 1 << 7
    priority_speaker = 1 << 8
    stream = 1 << 9
    view_channel = 1 << 10
    send_messages = 1 << 11
    send_tts_messages = 1 << 12
    manage_messages = 1 << 13
    embed_links = 1 << 14
    attach_files = 1 << 15
    read_message_history = 1 << 16
    mention_everyone = 1 << 17
    use_external_emojis = 1 << 18
    view_guild_insights = 1 << 19
    connect = 1 << 20
    speak = 1 << 21
    mute_members = 1 << 22
    deafen_members = 1 << 23
    move_members = 1 << 24
    use_vad = 1 << 25
    change_nickname = 1 << 26
    manage_nicknames = 1 << 27
    manage_roles = 1 << 28
    manage_webhooks = 1 << 29
    manage_emojis_and_stickers = 1 << 30
    use_application_commands = 1 << 31
    request_to_speak = 1 << 32
    manage_events = 1 << 33
    manage_threads = 1 << 34
    create_public_threads = 1 << 35
    create_private_threads = 1 << 36
    use_external_stickers = 1 << 37
    send_messages_in_threads = 1 << 38
    use_embedded_activities = 1 << 39
    moderate_members = 1 << 40


class UserFlags(Flags):
    staff = 1 << 0
    partner = 1 << 1
    hypesquad = 1 << 2
    bug_hunter_level_1 = 1 << 3
    hypesquad_one_house_1 = 1 << 6
    hypesquad_one_house_2 = 1 << 7
    hypesquad_one_house_3 = 1 << 8
    premium_early_supporter = 1 << 9
    team_pseudo_user = 1 << 10
    bug_hunter_level_2 = 1 << 14
    verified_bot = 1 << 16
    verified_developer = 1 << 17
    certified_moderator = 1 << 18
    bot_http_interactions = 1 << 19
