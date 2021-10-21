import aiohttp

base_url = "https://discord.com/api/v9"

class Message:
    def __init__(self, token: str, channel_id:int = None, message_id = None, content = None):
        self.message_id = message_id
        self.channel_id = channel_id
        self.token = token
        self.content = {"content": f"{content}"}

    async def edit(self, channel_id, message_id, content):
        msg = {"content": content}
        ch_id = channel_id
        msg_id = message_id
        headers = {"Authorization": f"Bot {self.token}"}
        async with aiohttp.ClientSession(headers = headers) as ses:
            async with ses.patch(url = f"{base_url}/channels{ch_id}/messages/{msg_id}", json = msg):
                pass