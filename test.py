import asyncio
import os
import traceback
import discode
from discode import commands
TOKEN = os.environ["BOT_TOKEN"]

client = commands.Bot(
    prefix = "d!",
    intents = discode.Intents.default()
)

def get_latency():
    return round((client.latency * 1000), 2)

@client.on_event("ready")
async def ready():
    print(f"{client.user} is ready!")
    print(f"Intents Int: {client.http.ws.intents.value}")


@client.on_event("message")
async def on_message(message: discode.Message):
    print(message.author, "has sent:\n", message.content)
    print(f"\nComponents: {message.components}")
    channel: discode.TextChannel = message.channel
    msg = message.content
    print(message.author.id)
    if msg.startswith("d!"):
        if msg.startswith("ping", len("d!")):
            latency = get_latency()
            embed: discode.Embed = discode.Embed(
                title = "Pong!",
                colour = discode.Colour.red()
            ).add_field(
                name = "My websocket ping",
                value = f"{latency}ms"
            ).set_footer(
                f"Requested by {message.author}"
            )
            await channel.send(embed = embed)

        elif msg.startswith("comp", len("d!")):
            comps = []
            button1 = discode.Button(discode.ButtonStyle.primary, label = "Hi")
            comps.append(button1)
            msg = await channel.send(
                "Component test.",
                components = comps
            )
            await asyncio.sleep(10)
            await msg.delete(reason = "Component test")

        elif msg.startswith("url", len("d!")):
            comps = [discode.Button(style = discode.ButtonStyle.url, url = "https://youtube.com/", label = "YouTube")]
            await channel.send("Go to YouTube", components = comps)

        elif msg.startswith("eval", len("d!")):
            if message.author.id not in [859996173943177226, 739443421202087966, 551257232143024139]:
                return await channel.send("Only owners can do this sus")
            try:
                data = msg[6:]
                data = ";".join(data.splitlines())
                args = {
                    "discode": discode,
                    "message": message,
                    "bot": client,
                    "client": client
                }
                exec(f"async def func():{data}", args)
                resp = await eval("func()", args)
                await channel.send(resp)
            except:
                error = traceback.format_exc()
                errorEm = discode.Embed(
                    title = "Error while excecuting code!",
                    description = f"```py\n{error}```"
                )
                await channel.send(embed = errorEm)

@client.on_event("message edit")
async def message_edit(before: discode.Message, after: discode.Message):
    if before.author.bot:
        return
    print(
        "Message edited by", after.author,
        "\nOld content:", before.content,
        "\nNew content:", after.content
    )

client.start(TOKEN)
