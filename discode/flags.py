from __future__ import annotations

from typing import Any, Dict, Iterator, Optional, Tuple, Type, Union

__all__ = ("Intents",)


class Flags:

    __items__: Dict[str, int]
    __settings__: Dict[str, Any]

    def __init__(self, value: int = 0, **flags):
        self.value: int = value

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
            if not k.startswith("_"):
                items[k] = v

        cls.__items__ = items

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
    direct_messages_typing = 1 << 14
    guild_scheduled_events = 1 << 16

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} value={self.value}>"

    @classmethod
    def all(cls) -> Intents:
        return cls(
            sum(
                (
                    v
                    for k, v in cls.__items__.items()
                    if (isinstance(v, int) and k != "value")
                )
            )
        )

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
    certified_developer = 1 << 18
    bot_http_interactions = 1 << 19
