
import os
import discode

TOKEN = os.environ.get

client = discode.Client(
    token=TOKEN,
    intents=discode.Intents.default()
)


@client.on_event("ready")
async def on_ready():
    print(client.user, "is ready!")


@client.on_event(discode.GatewayEvent.MESSAGE_CREATE)
async def on_message(message):
    msg: str = msg.content
    if msg.startswith("?hi"):
        await message.channel.send("Hi!!!")
