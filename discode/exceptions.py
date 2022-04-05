from __future__ import annotations

import typing

class DiscodeException(Exception):
    r"""The base exception for all :class:`Exception`s provided by Discode. All exceptions provided by Discode are subclassed from this class. This can be used to check if the error was raised by Discode.
    """
    ...

class HTTPException(DiscodeException):
    r"""The base exception for all http errors provided by Discode. This can be used to check whether the exception was raised due to an http error.
    """

    def __init__(self, *args: typing.Any, code: int):
        self.code: int = code
        super().__init__(*args)


class BadRequest(HTTPException):
    def __init__(self, *args: typing.Any):
        super().__init__(*args, code = 400)

class Unauthorized(HTTPException):
    def __init__(self, *args: typing.Any):
        super().__init__(*args, code = 401)

class Forbidden(HTTPException):
    def __init__(self, *args: typing.Any):
        super().__init__(*args, code = 403)

class NotFound(HTTPException):
    def __init__(self, *args: typing.Any):
        super().__init__(*args, code = 404)

class TooManyRequests(HTTPException):
    def __init__(self, *args: typing.Any):
        super().__init__(*args, code = 429)

HTTPCODES = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    429: TooManyRequests,
}

def http_error(code: int, *args: typing.Any) -> typing.Literal[
    BadRequest,
    Unauthorized,
]:
    return HTTPCODES[code](*args) if code in HTTPCODES else None

