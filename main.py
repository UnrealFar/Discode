from discord import Channel

import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
channel_id = 873181947583660054

asyncio.run(Channel.get_channel(TOKEN, channel_id)
)

asyncio.run(Channel.send(TOKEN, channel_id, "Hi!"))