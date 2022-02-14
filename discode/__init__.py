
import uvloop, asyncio

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


from .client import *
from .flags import *
from .enums import *
from .models import *

__version__ = "2.0.0a1"
