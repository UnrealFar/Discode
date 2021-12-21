class Intents:
    r"""Discord requires you to set the amount of gateway intents your bot uses."""

    def __init__(self, **intents):
        self.value = 0

        for k, v in intents.items():
            if v:
                intent = getattr(self, k, None)
                if not intent:
                    raise ValueError(f"Intent called {k} does not exist!")

                intent

    @classmethod
    def default(cls):
        kwargs = {
            "guilds": True,
            "messages": True,
            "members": True,
            "reactions": True,
            "typing": True,
            "emojis": True,
            "invites": True,
            "events": True,
        }
        return cls(**kwargs)

    @classmethod
    def all(cls: "Intents"):
        i = cls()
        i.value = 32767
        return i

    @property
    def guilds(self):
        self.value += 1 << 0
        return self

    @property
    def members(self):
        self.value += 1 << 1
        return self

    @property
    def bans(self):
        self.value += 1 << 2
        return self

    @property
    def emojis(self):
        self.value += 1 << 3
        return self

    @property
    def integrations(self):
        self.value += 1 << 4
        return self

    @property
    def webhooks(self):
        self.value += 1 << 5
        return self

    @property
    def invites(self):
        self.value += 1 << 6
        return self

    @property
    def voice_states(self):
        self.value += 1 << 7
        return self

    @property
    def presence(self):
        self.value += 1 << 8
        return self
    
    @property
    def guild_messages(self):
        self.value += 1 << 9
        return self
    
    @property
    def direct_messages(self):
        self.value += 1 << 12
        return self

    @property
    def messages(self):
        self.value += ((1 << 9) + (1 << 12))
        return self

    @property
    def reactions(self):
        self.value += 1 << 10
        self.value += 1 << 13
        return self

    @property
    def typing(self):
        self.guild_typing
        self.dm_typing
        return self

    @property
    def guild_typing(self):
        self.value += 1 << 11
        return self

    @property
    def dm_typing(self):
        self.value += 1 << 14
        return self

    @property
    def events(self):
        self.value += 1 << 15
        return self
