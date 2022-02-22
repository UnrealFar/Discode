# Discode
Discode is an asynchronous Python API wrapper for the Discord REST and Gateway API. This project was inspired by [Discord.py](https://github.com/rapptz/discord.py) and may contain similar functioning.

### Basic Example Usage
```py
import discode

client = discode.Client(token = "YOUR-TOKEN-HERE")

@client.on_event(discode.GatewayEvent.READY)
async def ready():
    print(f"{client.user} is ready!")

@client.on_event(discode.GatewayEvent.MESSAGE_CREATE)
async def message(message: discode.Message):
    content = message.content
    if content.startswith("?hi"):
        await message.channel.send("Hiii!!!")

client.run()
```