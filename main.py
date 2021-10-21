import discord
from discord import Client
from discord import Channel
from discord import Embed

import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

client = Client(TOKEN)
test_channel_id = 873181947583660054
channel = Channel(test_channel_id, Client.get_token)

embed = Embed(title = "Hello!", description = "Hi!", colour = discord.Colour.red)
embed.create_field(name = "This is a field name", value = "This is a field value")

asyncio.run(channel.send(message = "Hi!", embed = embed))

client.run()