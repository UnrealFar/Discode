import aiohttp
import asyncio

class Route:

    def __init__(
        self
        ):
        self.version: int = 9
        self.url = f"{self.base_url}/v{self.version}/{self.path}"

    @property
    def bucket(self) -> str:
        return

class HTTPClient:
  
    def __init__(
        self,
        token: str
    ):
        self.token = token

    async def request(
        self,
        method: str,
        path: str,
        json = None,
        headers = None
        ):
        base_url: str = "https://discord.com/api"
        url = base_url + path
        headers: dict = {}

        if self.token is not None:
            headers["Authorization"] = "Bot " + self.token

        if method.lower() == "get":
            async with aiohttp.ClientSession() as session:
                async with session.get(url = url, json = json, headers = headers) as response:
                    data = await response.json()
                    return data

        elif method.lower() == "post":
            async with aiohttp.ClientSession() as session:
               async with session.post(url = url, json = json, headers = headers) as response:
                    data = await response.json()
                    return data

        elif method.lower() == "patch":
            async with aiohttp.ClientSession() as session:
                async with session.patch(urle = url, json = json, headers = headers) as response:
                    data = await response.json()
                    return data