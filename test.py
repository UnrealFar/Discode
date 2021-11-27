import asyncio
import discode
import os

TOKEN = os.environ["BOT_TOKEN"]

client = discode.Client(
    loop = asyncio.get_event_loop(),
    intents = 512
)

@client.on_event("ready")
async def ready():
    print(f"{client.user} is ready!")

@client.on_event("message")
async def on_message(message: discode.Message):
    print(message.author, "has sent:\n", message.content)

@client.on_event("message edit")
async def message_edit(before: discode.Message, after: discode.Message):
    print(
        "Message edited by", after.author,
        "\nOld content:", before.content,
        "\nNew content:", after.content
    )

client.start(TOKEN)