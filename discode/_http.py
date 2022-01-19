import asyncio
from typing import Optional, Union
import aiohttp

from .user import ClientUser, User
from .intents import Intents
from .message import Message
from .channel import TextChannel
from .guild import Guild
from .components import ActionRow
from . import gw
from .errors import (
    HTTPError,
    Unauthorized,
    Forbidden,
    BadRequest,
    DiscodeError,
    DiscordError
)

class HTTP:
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_event_loop(), **kwargs):
        self.loop: asyncio.AbstractEventLoop = loop
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.client: ClientUser = kwargs.get("client")
        self.api_url = "https://discord.com/api/v9"
        self.intents: Intents = kwargs.get("intents")
        self.user_agent = "DiscordBot made with Discode"

    async def request(self, method: str, endpoint: str, **kwargs):
        if not kwargs.get("headers"):
            headers = {"Authorization": "Bot " + self.token}
        else:
            headers = kwargs.pop("headers", {})
            headers["Authorization"] = "Bot " + self.token

        async with self.session.request(
            method = method,
            url = self.api_url + endpoint,
            headers = headers,
            **kwargs
        ) as resp:

            if resp.status in (200, 204):
                if resp.status == 200:
                    return await resp.json()

            elif resp.status >= 400 > 500:
                if resp.status == 400:
                    raise BadRequest(await resp.text())

                elif resp.status == 401:
                    raise Unauthorized(await resp.text())

                elif resp.status == 403:
                    raise Forbidden(await resp.text())

            elif resp.status >= 500:
                raise DiscordError(await resp.text())

            else:
                err = f"Something unknown happened while trying to make a {method.lower()} request to {self.api_url + endpoint}"
                try:
                    data = await resp.json()
                    data = data.pop("message", data)
                except:
                    data = await resp.text()
                raise HTTPError(err, data, code = resp.status)

    async def connect(self):
        if self.session.closed:
            self.session = aiohttp.ClientSession()

        data = {
            "loop": self.loop,
            "token": self.token,
            "intents": self.intents,
            "http": self,
            "dispatch": self.client.dispatch,
        }
        self.ws = gw.WS(data)
        await self.ws.handle()

    async def login(self, token: str):
        self.token = token
        try:
            data = await self.request("GET", "/users/@me")
        except:
            raise

        data["http"] = self
        self.user = ClientUser(**data)

        return self.user

    async def close(self):
        if not self.session.closed:
            await self.session.close()

    async def send_message(self, channel_id, *content, **kwargs) -> Message:
        data = {}

        if len(content) >= 1:
            data["content"] = str().join((str(content) for content in content))

        if kwargs.get("embed", None):
            data["embeds"] = [kwargs.pop("embed").get_payload()]

        if kwargs.get("embeds", None):
            if "embeds" not in data:
                data["embeds"] = []
            embeds = kwargs.pop("embeds")
            for embed in embeds:
                data["embeds"].append(embed.get_payload())

        if kwargs.get("components", None):
            rows = []
            data["components"] = []
            for component in kwargs["components"]:
                if not isinstance(component, ActionRow):
                    if hasattr(component, "url"):
                        if not component.url:
                            self.client.active_interactions.append(component)
 
                    else:
                        self.client.active_interactions.append(component)
                    if component.row:
                        component.row.items.append(component)
                    else:
                        if len(rows) == 0:
                            rows.append(ActionRow())
                        for row in rows:
                            if len(row.items) >= 5:
                                row = ActionRow()
                                rows.append(row)
                            row.items.append(component)
                            break

            for row in rows:
                data["components"].append(row.get_payload())

        msgdata = await self.request("POST", f"/channels/{channel_id}/messages", json=data)
        msgdata["http"] = self
        return Message(**msgdata)

    async def fetch_user(self, user_id: int) -> User:
        data = await self.request(
            "GET",
            f"/users/{user_id}"
        )
        data["http"] = self
        return User(**data)

    async def fetch_channel(self, channel_id: int) -> Union[TextChannel]:
        data = await self.request("GET", f"/channels/{channel_id}")
        data["http"] = self
        return TextChannel(**data)

    async def fetch_guild(self, guild_id: int) -> Guild:
        data = await self.request("GET", f"/guilds/{guild_id}")
        data['http'] = self
