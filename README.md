# Discode
A Discord API wrapper that is currently under development and is not ready for full release and general use.

### Basic Example Usage
```py
import discode

client = discode.Client()
# You can specify an event loop
# in the parameters of discode.Client

# the coroutine under the decorator
# can have any name you wish to use
@client.on_event("ready")
async def ready():
    print(f"{client.user} is ready!")

@client.on_event("message")
async def message(message: discode.Message):
    print(message.content)

client.start()
```