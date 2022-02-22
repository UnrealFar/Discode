
import uvloop, asyncio

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def __get_event_loop():
  try:
    return asyncio.get_running_loop()
  except RuntimeError:
    return asyncio.new_event_loop()

asyncio.get_event_loop = __get_event_loop

from .client import *
from .flags import *
from .enums import *
from .models import *

__version__ = "2.0.0a2"
