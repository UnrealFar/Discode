import asyncio
import textwrap
import traceback
import json

import discode

with open("env.json", "r") as env_file:
    env = json.load(env_file)
    token = env.get("BOT_TOKEN")

bot = discode.Client(token=token)


def get_info():
    ret = f"Intents: {bot.intents.value}\nLatency: {round(bot.latency * 1000, 2)}ms\nGuilds: {len(bot.guilds)}\nUsers: {len(bot.users)}"
    return ret


@discode.utils.async_function
def pront(*args):
    return print(*args)


@bot.on_event(discode.GatewayEvent.READY)
async def on_ready():
    print(get_info())
    print(client.user, "is ready!")

@bot.on_event(discode.GatewayEvent.MESSAGE_CREATE)
async def on_message(message: discode.Message):
    await pront(message.author, ":", message)
    msg = message.content

    if msg.startswith("d!hi"):
        await message.channel.send("Hi!")

        async def hi_check(_message: discode.Message):
            if (
                _message.content.lower() == "hello"
                and _message.author_id == message.author_id
            ):
                await _message.channel.send("Hulloo!")
                return True

        try:
            await bot.wait_for("message_create", check=hi_check)
        except:
            pass

    elif msg.startswith("d!invite"):
        embed = discode.Embed(title="Invite Discode!", description=bot.invite_url)
        await message.channel.send(embeds=(embed,))

    elif msg.startswith("d!eval"):
        if message.author.id not in [
            859996173943177226,
            739443421202087966,
            551257232143024139,
            685082846993317953,
        ]:
            return await message.channel.send("Only owners can do this sus")
        try:
            data = msg[6:]
            args = {
                **globals(),
                "message": message,
                "author": message.author,
                "channel": message.channel,
                "guild": message.guild,
                "client": bot,
                "imp": __import__,
            }
            data = data.replace("return", "yield").replace("”", '"').replace("“", '"')
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
            await message.channel.send(
                embed=discode.Embed(
                    title="Uh Oh!",
                    description=f"```py\n{error}```",
                )
            )


bot.run()
