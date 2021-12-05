r"""Discode
---------
Discode is a modern asynchronous Python API wrapper for the Discord REST API and the Discord Gateway API. We try our best to prevent 429s by ratelimit handlers and cacheing data when we can. Discode is currently in alpha development stage.

LICENSE
---------
MIT License

Copyright (c) 2021-Present TheFarGG

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Literal, NamedTuple

from .client import *
from .user import *
from .message import *
from .intents import *
from .channel import *
from .bot import *
from .guild import *
from .errors import *
from .embeds import *
from .member import *
from .colours import *
from .enums import *
from .components import *

__name__ = "Discode"
__author__ = "TheFarGG"
__copyright__ = "Copyright (c) 2021-present TheFarGG"
__version__ = "0.0.2a"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    level: Literal["alpha", "beta", "final"]


version_info = VersionInfo(major=0, minor=0, micro=2, level="alpha")

