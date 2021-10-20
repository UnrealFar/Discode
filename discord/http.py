import aiohttp

class Route:

    def __init__(
        self,
        method: str,
        path: str
        ):
        self.method: str = method
        self.version: int = 9
        self.path: str = path
        self.base_url: str = "https://discord.com/api"
        self.url = f"{self.base_url}/v{self.version}/{self.path}"

    @property
    def bucket(self) -> str:
        return

class HTTPClient:
  
    def __init__(
        self,
        token: str,
        params: str
    ):
        self.params = params
        self.token = token
        self.__session: aiohttp.ClientSession

    async def request(
        self,
        route: Route
        ):
        url = route.url
        method = route.method
        headers: dict = {}

        if self.token is not None:
            headers["Authorization"] = "Bot " + self.token

        async with self.__session.request(method, url) as response:
            data = await response

            if 300 > response.status >= 200:
                return data

            if response.status == 429:
                return "Ratelimit exceeded!"

    async def static_login(self, token: str):
        self.__session = aiohttp.ClientSession()
        old_token = self.token
        self.token = token

        try:
            data = await self.request(Route("GET", "/users/@me"))

        except Exception as e:
            self.token = old_token
            if e.status == 401:
                raise "Improper Token Passed!"
            raise

        return data

    def logout(self):
        return self.request(Route("POST", "/auth/logout"))