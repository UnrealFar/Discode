from typing import Literal, NamedTuple

from .client import *
from .user import *
from .message import *
from .intents import *
from .channel import *
from .bot import *
from .guild import *
from .errors import *

__name__ = "Discode"
__author__ = "TheFarGG"
__copyright__ = "Copyright 2021-present TheFarGG"
__version__ = "0.0.0"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    level: Literal["alpha", "beta", "final"]


version_info = VersionInfo(major=0, minor=0, micro=1, level="alpha")
