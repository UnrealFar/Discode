import asyncio
import discode
import os

TOKEN = os.environ["BOT_TOKEN"]

client = discode.Client(
    loop = asyncio.get_event_loop()
)

@client.event
async def on_ready():
    print(f"{client.user}is ready!")

client.start(TOKEN)