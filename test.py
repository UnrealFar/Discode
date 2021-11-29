import asyncio
import discode
import os
import json


TOKEN = os.environ["BOT_TOKEN"]

client = discode.Bot(
    prefix = "d!",
    intents = discode.Intents.default()
)

def get_latency():
    return round((client.latency * 1000), 2)

@client.on_event("ready")
async def ready():
    print(f"{client.user} is ready!")
    latency = get_latency()
    print(f"My latency is {latency}ms")
    print(f"Intents Int: {client.http.ws.intents.value}")


@client.on_event("message")
async def on_message(message: discode.Message):
    print(message.author, "has sent:\n", message.content)
    msg = message.content
    if msg.startswith("d!"):
        channel = message.channel
        if msg.startswith("ping", len(client.prefix)):
            latency = get_latency()
            await channel.send(f"{latency}ms")
        elif msg.startswith("eval", len(client.prefix)):
            if message.author.id not in [859996173943177226, 739443421202087966]:
                return await channel.send("Only owners can do dis...")
            try:
                data = msg[len(client.prefix):][4:]
                exec(f"async def func():{data}")
                resp = await eval("func()")
                await channel.send(resp)
            except Exception as error:
                await channel.send(f"Error while excecuting code!\n{str(error)}")

    elif msg.startswith("GUILD_TEST"):
        for guild_id in client.guild_cache:
            guild = client.guild_cache[message.guild_id]
            print(guild.channels)

@client.on_event("message edit")
async def message_edit(before: discode.Message, after: discode.Message):
    print(
        "Message edited by", after.author,
        "\nOld content:", before.content,
        "\nNew content:", after.content
    )

client.start(TOKEN)
