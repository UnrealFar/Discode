class Embed:
    def __init__(self, title = None, description = None):
        self.title = title
        self.description = description
        self.embed = {
            "title": title,
            "description": description
        }

    @property
    def get_embed(self):
        return self.embed

    def create_field(self, name: str, value: str, inline: bool= False):
        field = {
            "name": name,
            "value": value,
            "inline": inline
        }
        try:
            self.embed["fields"].append(field)
        except:
            self.embed["fields"] = [field]