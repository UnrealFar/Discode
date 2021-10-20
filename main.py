from discord import Channel
from discord import Message
import discord

import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

client = discord.Client()
test_channel_id = 873181947583660054

#client.run(TOKEN)

asyncio.run(client.start(TOKEN))