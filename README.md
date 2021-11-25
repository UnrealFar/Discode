# Discode
A Discord API wrapper that is not yet ready for general use

**Example Usage**
```py
import discode

client = discode.Client()

@client.event
async def on_ready():
    print(f"{client.user} is ready!")

client.start()
```
