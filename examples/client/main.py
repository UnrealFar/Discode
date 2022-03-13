import os

import discode

TOKEN = os.environ.get("TOKEN")
# The token from the developer portal.

client = discode.Client(token=TOKEN, intents=discode.Intents.default())


@client.on_event("ready")
async def on_ready():
    print(client.user, "is ready!")


# The ready listener gets fired when the bot/client is completely ready for use.


@client.on_event("message_create")
async def on_message(message: discode.Message):
    msg: str = msg.content
    if msg.startswith("?hi"):
        await message.channel.send("Hi!!!")


# The message_create listener is fired whenever a message is sent to any channel that the bot has access to.
