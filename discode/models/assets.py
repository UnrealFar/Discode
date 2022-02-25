from __future__ import annotations

from .abc import Asset as _Asset

__all__ = ("Asset",)

class Asset(_Asset):
    r"""
    Represents a Discord Asset. An asset can be either of the following: `user avatar`, `user banner`, `guild icon`, `guild banner`.
    """

    __slots__ = ("_url", "_key", "_animated", "_connection")

    def __init__(self, connection, *, url: str, key: str, animated: bool = False):
        self._url = url
        self._key = key
        self._animated = animated

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._url == other._url

    def __hash__(self):
        return hash(self._key)

    @classmethod
    def user_avatar(cls: Asset, user) -> Asset:
        av = user._avatar
        an = av.startswith("a_")
        ext = "gif" if an else "png"
        return cls(
            user._connection,
            url=f"{cls.BASE_URL}/avatars/{user.id}/{av}.{ext}?size=1024",
            key=av,
            animated=an,
        )

    @classmethod
    def user_banner(cls: Asset, user) -> Asset:
        ba = user._banner
        an = ba.startswith("a_")
        ext = "gif" if an else "png"
        return cls(
            user._connection,
            url=f"{cls.BASE_URL}/banners/{user.id}/{ba}.{ext}?size=1024",
            key=ba,
            animated=an,
        )

    @classmethod
    def guild_icon(cls: Asset, guild) -> Asset:
        ic = guild._icon
        an = ic.startswith("a_")
        ext = "gif" if an else "png"
        
        return cls(
            guild._connection,
            url=f"{cls.BASE_URL}/icons/{guild.id}/{ic}.{ext}?size=1024",
            key=ic,
            animated=an,
        )

    @property
    def url(self) -> str:
        r""":class:`str`: Returns the url of the asset."""
        return self._url

    @property
    def key(self) -> str:
        r""":class:`str`: Returns the identifying key of the asset."""
        return self._key

    @property
    def animated(self) -> bool:
        r""":class:`bool`: Returns :class:`True` if the asset is animated else :class:`False`"""
        return self._animated
