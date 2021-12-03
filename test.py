import asyncio
import discode
import os
from discode import Embed, Colour

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
    print(f"\nComponents: {message.components}") if message.components != [] else None
    channel: discode.TextChannel = message.channel
    msg = message.content
    print(message.author.id)
    if msg.startswith("d!"):
        if msg.startswith("ping", len(client.prefix)):
            latency = get_latency()
            embed: Embed = Embed(title = "Pong!", colour = Colour.red()).add_field(
                name = "My websocket ping",
                value = f"{latency}ms"
            ).set_footer(f"Requested by {message.author}")
            await channel.send(embed = embed)

        elif msg.startswith("eval", len(client.prefix)):
            if message.author.id not in [859996173943177226, 739443421202087966, 551257232143024139]:
                return await channel.send("Only owners can do dis...")
            try:
                data = msg[len(client.prefix):][4:]
                args = {
                    "discode": discode,
                    "message": message,
                    "bot": client,
                    "client": client,
                    "import": __import__
                }
                exec(f"async def func():{data}", args)
                resp = await eval("func()", args)
                await channel.send(resp)
            except Exception as error:
                await channel.send(f"Error while excecuting code!\n{str(error)}")

@client.on_event("message edit")
async def message_edit(before: discode.Message, after: discode.Message):
    print(
        "Message edited by", after.author,
        "\nOld content:", before.content,
        "\nNew content:", after.content
    )

client.start(TOKEN)
