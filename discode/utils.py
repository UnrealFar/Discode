import pprint

from .message import Message
from .member import Member

def make_pretty(*args, **kwargs) -> str:
    return pprint.pformat(*args, **kwargs)

async def _check(ws, data: dict):
    if ws._ready.is_set():
        event = data.get('t').upper()
        d = data.get("d")
        if event == "MESSAGE_CREATE":
            msgdata = data["d"]
            msgdata["http"] = ws.http
            message = Message(**msgdata)
            ws.message_cache.append(message)
            if len(ws.message_cache) == ws.http.client.message_limit:
                ws.message_cache[1:]
            await ws.dispatch("message", message)

        elif event == "MESSAGE_UPDATE":
            for msg in ws.message_cache:
                if msg.id == int(d.get("id")):

                    msgdata = msg.data.copy()
                    before = msg
                    after = Message(**msgdata)
                    after.content = data["d"].get("content")
                    msg.data["edited_at"] = data["d"].get("edited_timestamp")
                    await ws.dispatch("message edit", before, after)
                    ws.message_cache.remove(before)
                    ws.message_cache.append(after)
                    break

        elif event == "MESSAGE_DELETE":
            for msg in ws.message_cache:
                pass

        elif event == "MEMBER_ADD":
            for g in ws.guilds:
                if g.id == int(d.get("guild_id")):
                    d.pop("guild_id", None)
                    g.members.append(d)
                    await ws.dispatch("member create")
                    break

        elif event == "MEMBER_DELETE":
            g = ws.client.get_guild(int(d.get("guild_id")))
            if not g:
                return

        elif event == "MEMBER_UPDATE":
            g = ws.client.get_guild(int(d.get("guild_id")))
            if g:
                d.pop("guild_id", None)
                m = ws.client.get_member(
                    member_id = int(d.get("id")),
                    guild_id = g.id
                )
                try:
                    g.members.remove(m)
                except ValueError:
                    pass
                g.members.append(d)
