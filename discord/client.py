import aiohttp
import asyncio
import signal

from .http import HTTPClient

base_url = "https://discord.com/api/v9"

class Client:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None
    ):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.http = HTTPClient

    async def login(self, token: str):
        await self.http.static_login(token.strip())

    async def start(self, token: str):
        await self.login(token = token)

    def run(self, token: str):
        loop = self.loop

        try:
            loop.add_signal_handler(signal.SIGINT, lambda: loop.stop())
            loop.add_signal_handler(signal.SIGTERM, lambda: loop.stop())

        except:
            pass

        async def runner():
            try:
                await self.start(token)
            except:
                pass

        def stop_loop_on_completion(f):
            loop.stop()

        future = asyncio.ensure_future(runner(), loop = loop)
        future.add_done_callback(stop_loop_on_completion)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            raise
        finally:
            future.remove_done_callback(stop_loop_on_completion)

        if not future.cancelled():
            try:
                return future.result()
            except KeyboardInterrupt:
                return None