import logging
import textwrap
import traceback
import json
import os

import discode

with open("env.json", "r") as env_file:
    env = json.load(env_file)
    token = env.get("BOT_TOKEN", os.environ.get("BOT_TOKEN"))

owner_ids = (
    859996173943177226,
    739443421202087966,
    551257232143024139,
    685082846993317953,
    611448893904781312,
)
bot = discode.Client(token=token)
logger = logging.getLogger("discode")
logger.setLevel(logging.DEBUG)


def get_info():
    ret = f"Intents: {bot.intents.value}\nLatency: {round(bot.latency * 1000, 2)}ms\nGuilds: {len(bot.guilds)}\nUsers: {len(bot.users)}"
    return ret


@discode.utils.async_function
def run_docs(make=False):
    if make:
        os.system("cd docs\nmake html\ncd\ncd discode")
    return os.system("python -m http.server -d docs/_build/html")


@bot.on_event(discode.GatewayEvent.READY)
async def on_ready():
    print(get_info())
    print(bot.user, "is ready!")
    bot.loop.create_task(run_docs(make=True))


@bot.on_event(discode.GatewayEvent.MESSAGE_CREATE)
async def on_message(message: discode.Message):
    print(message.author, ":", message)
    msg = message.content

    if msg.startswith("d!choose"):
        channel = message.channel
        await channel.send("Choose between foo and bar!")

        async def hi_check(_message: discode.Message):
            choice = str(_message).lower()
            if (
                (choice in ("foo", "bar"))
                and _message.author_id == message.author_id
                and _message.channel_id == channel.id
            ):
                await channel.send(f"Your choice is {choice}!")
                return True

        try:
            await bot.wait_for("message_create", check=hi_check)
        except:
            await channel.send("You did not reply in time!")

    elif msg.startswith("d!invite"):
        embed = discode.Embed(title="Invite Discode!", description=bot.invite_url)
        await message.channel.send(embeds=(embed,))

    elif msg.startswith("d!ratelimit"):
        channel = message.channel
        if message.author_id not in owner_ids:
            return await channel.send("Only owners can do this sus")
        for r in range(10):
            await channel.send(r + 1)

    elif msg.startswith("d!eval"):
        if message.author_id not in owner_ids:
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
