import discode

client = discode.Client(
    message_limit = 50,
    intents = discode.Intents.default()
)

@client.on_event("ready")
async def on_ready():
    print(client.user, "is ready!")

@client.on_event("message")
async def on_message(message):
    msg: str = msg.content
    if msg.startswith("?hi"):
        await message.channel.send("Hi!!!")
