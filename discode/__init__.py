r"""
Discode
-------

Discode is an asynchronous API wrapper for the Discord API.
It provides all necessary functionalities needed to interact with Discord bot developing and other functions of the API. It also provides utilities to make coding with Discode much easier.
"""

__all__ = (
    "Client",
    "Embed",
    "File",
    "GatewayEvent",
    "ButtonStyle",
    "Intents",
    "Permissions",
    "UserFlags",
    "Snowflake",
    "Asset",
    "TextChannel",
    "DMChannel",
    "Guild",
    "Member",
    "Message",
    "Role",
    "User",
    "Button",
    "LinkButton",
)

import asyncio
import platform

try:
    import uvloop
except:
    if "linux" in str(platform.platform()).lower():
        print(
            "UVLoop is supported on Linux devices. Please install it for better performance!"
        )
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def __get_event_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.new_event_loop()


asyncio.get_event_loop = __get_event_loop

from .client import *
from .dataclasses import *
from .enums import *
from .flags import *
from .models import *
from .app import *

__version__ = "2.0.0b2"
