from .user import User

class Member:
    r"""Represents a Discord guild member.
    """
    def __init__(self, **data):
        self.data = data
        self.http = data.get("http")
        self.id = int(self.user.id)

    def __str__(self) -> str:
        return f"{self.name}#{self.discriminator}"

    @property
    def name(self) -> str:
        return self.user.name

    @property
    def discriminator(self) -> int:
        return int(self.user.discriminator)

    @property
    def nick(self) -> str:
        return self.data.get("nick")

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"

    @property
    def display_name(self) -> str:
        if not self.nick:
            return self.name
        return self.nick

    @property
    def roles(self):
        return self.data.get("roles")

    @property
    def joined_at(self):
        return self.data.get("joined_at")

    @property
    def user(self) -> User:
        if not hasattr(self, "_user"):
            data = self.data.get("user")
            data["http"] = self.http
            self._user = User(**data)
        return self._user

