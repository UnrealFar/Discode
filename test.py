import os, asyncio, traceback, textwrap

import discode

token = os.environ.get("BOT_TOKEN")

bot = discode.Client(token=token)
kws = ["and, as, assert, async, await, break, class, continue, def, del, elif, else, except, finally, for, from, global, if, import, in, is, lambda, nonlocal, not, or, pass, raise, return, try, while, with, yield, e"]

def get_info():
    return f"Intents: {bot.intents}\nLatency: {round(bot.latency * 1000, 2)}ms\nGuilds: {len(bot.guilds)}\nUsers: {len(bot.users)}\n{bot.user} is ready!"

@bot.on_event(discode.GatewayEvent.READY)
async def on_ready():
    print(get_info())

@bot.on_event(discode.GatewayEvent.MESSAGE_CREATE)
async def on_message(message: discode.Message):
    print(message.author, ":", message)
    msg = message.content

    if msg.startswith("d!hi"):
        await message.channel.send("Hi!")

    elif msg.startswith("eval", len("d!")):
        if message.author.id not in [859996173943177226, 739443421202087966, 551257232143024139, 685082846993317953]:
            return await message.channel.send("Only owners can do this sus")
        try:
            data = msg[6:]
            args = {
                "discode": discode,
                "message": message,
                "author": message.author,
                "channel": message.channel,
                "guild": message.guild,
                "bot": bot,
                "client": bot,
                "imp": __import__,
                **globals()
            }
            data = data.replace("return", "yield")
            if data.startswith(" "):
                data = data[1:]
            for line in data.splitlines():
                for word in kws.split(", "):
                    if word not in line:
                        data = data.replace(line, f"yield {line}")
            data = textwrap.indent(data, "    ")
            exec(f"async def func():\n{data}", args)
            async for resp in eval("func()", args):
                resp = str(resp).replace(token, "[TOKEN]")
                await message.channel.send(resp)
        except:
            error = traceback.format_exc()
            await message.channel.send(f"```py\n{error}```")

bot.run()
