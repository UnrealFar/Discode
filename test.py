import os, asyncio

import discode

token = os.environ.get("BOT_TOKEN")

bot = discode.Client(token=token)

def get_info():
    return f"Intents: {bot.intents}\nGuilds: {len(bot.guilds)}\nUsers: {len(bot.users)}\n{bot.user} is ready!"

@bot.on_event("ready")
async def onready():
    print(get_info())

bot.run()
