import os, asyncio, traceback, textwrap

import discode

token = os.environ.get("BOT_TOKEN")

bot = discode.Client(token=token)

def get_info():
    return f"Intents: {bot.intents}\nLatency: {round(bot.latency * 1000, 2)}ms\nGuilds: {len(bot.guilds)}\nUsers: {len(bot.users)}\n{bot.user} is ready!"

@bot.on_event(discode.GatewayEvent.READY)
async def on_ready():
    await asyncio.sleep(5)
    print(get_info())

@bot.on_event(discode.GatewayEvent.MESSAGE_CREATE)
async def on_message(message: discode.Message):
    print(message.author, ":", message)
    msg = message.content

    if msg.startswith("d!hi"):
        await message.channel.send("Hi!")

    elif msg.startswith("eval", len("d!")):
        if message.author.id not in [859996173943177226, 739443421202087966, 551257232143024139]:
            return await message.channel.send("Only owners can do this sus")
        try:
            data = msg[6:]
            args = {
                "discode": discode,
                "message": message,
                "author": message.author,
                "channel": message.channel,
                "bot": bot,
                "client": bot,
                "imp": __import__,
                **globals()
            }
            exec(f"async def func():\n{textwrap.indent(data, '    ')}", args)
            resp = await eval("func()", args)
            resp = str(resp).replace(token, "[TOKEN]")
            await message.channel.send(resp)
        except:
            error = traceback.format_exc()
            await message.channel.send(f"```py\n{error}```")

bot.run()
