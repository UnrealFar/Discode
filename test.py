import os, asyncio, traceback, textwrap

import discode

token = os.environ.get("BOT_TOKEN")

bot = discode.Client(token=token)
kws = "and, as, assert, async, await, break, class, continue, def, del, elif, else, except, finally, for, from, global, if, import, in, is, lambda, nonlocal, not, or, pass, raise, return, try, while, with, yield, e"

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

        async def hi_check(_message: discode.Message):
            if _message.content.lower() == "hello" and _message.author_id == message.author_id:
                await _message.channel.send("Hulloo!")
                return True
        try:
            await bot.wait_for("message_create", check = hi_check)
        except:
            pass

    elif msg.startswith("d!invite"):
        embed = discode.Embed(
            title = "Invite Discode!",
            description = bot.invite_url
        )
        await message.channel.send(embeds = (embed,))

    elif msg.startswith("d!eval"):
        if message.author.id not in [859996173943177226, 739443421202087966, 551257232143024139, 685082846993317953]:
            return await message.channel.send("Only owners can do this sus")
        try:
            data = msg[6:]
            args = {"discode": discode, "message": message, "author": message.author, "channel": message.channel, "guild": message.guild, "bot": bot, "client": bot, "imp": __import__, **globals()}
            data = data.replace("return", "yield").replace('”', '"').replace('“', '"')
            if data.startswith(" "):
                data = data[1:]
            split = data.splitlines()
            if len(split) == 1:
                if not data.startswith("yield"):
                    data = f"yield {data}"
            data = textwrap.indent(data, "    ")
            exec(f"async def func():\n{data}", args)
            async for resp in eval("func()", args):
                resp = str(resp).replace(token, "[TOKEN]")
                await message.channel.send(resp)
        except:
            error = traceback.format_exc()
            await message.channel.send(embeds = (discode.Embed(title = "Uh Oh!", description = f"```py\n{error}```")))

bot.run()
