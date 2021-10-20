import aiohttp

class BaseCommand:
    slots = ()

class ApplicationCommand(BaseCommand):
    pass

class SlashCommand:
    def __init__(self, token:str , user_id: int):
        self.user_id = user_id
        self.token = token
        self.url = f"httpdiscord.com/api/v9/applications/{self.user_id}/commands"

    def slash_command():
        pass