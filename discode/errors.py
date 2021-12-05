

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

class Unauthorized(DiscodeError):
    r"""Raised when the API responds with a 401 status code. This happens when a client tries to authenticate with invalid / missing / incomplete credentials
    """

class Forbidden(DiscodeError):
    r"""Raised when the client receives a 403 Forbidden response status when it tries to request data that it doesn't have permission to access.
    """
    def __init__(self, *args):
        super().__init__(*args)

class BadRequest(DiscodeError):
    r"""Raised when the API sends a 404 response status to an http request made by a client. This occurs when the client tries to access to access content that doesn't exist.
    """
    def __init__(self, *args):
        super().__init__(*args)

