# Discode
A Discord API wrapper that is not yet ready for general use

**Usage**
```py
import discord

import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

client = discord.Client(TOKEN)

test_channel_id = 873181947583660054
channel = Channel(test_channel_id)

embed = discord.Embed(title = "Hello!", description = "Hi!", colour = discord.Colour.red())
embed.add_field(name = "This is a field name", value = "This is a field value")

asyncio.run(channel.send(message = "Hi!", embed = embed))
```
