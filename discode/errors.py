

class DiscodeError(Exception):
    r"""This is the default base for all the errors.
    """
    def __init__(self, *args):
        super().__init__(*args)

class InvalidToken(DiscodeError):
    r"""Raised when the user provides an invalid token.
    """
    def __init__(self, *args):
        super().__init__(*args)
