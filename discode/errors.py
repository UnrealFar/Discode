

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

# HTTP errors

class HTTPError(DiscodeError):
    r"""Base for errors raised when an error occurs during exchange of data with the REST API.
    """
    def __init__(self, *args, code: int = None):
        super().__init__(*args)

class Unauthorized(HTTPError):
    r"""Raised when the API responds with a 401 status code. This happens when a client tries to authenticate with invalid / missing / incomplete credentials
    """
    def __init__(self, *args):
        super().__init__(*args)

class Forbidden(HTTPError):
    r"""Raised when the client receives a 403 Forbidden response status when it tries to request data that it doesn't have permission to access.
    """
    def __init__(self, *args):
        super().__init__(*args)

class BadRequest(HTTPError):
    r"""Raised when the API sends a 404 response status to an http request made by a client. This occurs when the client tries to access to access content that doesn't exist.
    """
    def __init__(self, *args):
        super().__init__(*args)

class DiscordError(HTTPError):
    r"""Raised when the API sends a 500 status code. This occurs when there is an error in the Discord servers.
    """
    def __init__(self, *args):
        super().__init__(*args)

# Gateway Errors

class GatewayError(DiscodeError):
    r"""Base for errors raised when an error occurs with the gateway connection with Discord.
    """
    def __init__(self, *args):
        super().__init__(*args)

class PrivilegedIntentsRequired(GatewayError):
    r"""Raised when the client passes intents that require privileged intents to be explicitly enabled in the Discord Developer Portal.
    """
    def __init__(self, *args):
        super().__init__(*args)
