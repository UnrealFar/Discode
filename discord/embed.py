class Embed:
    def __init__(self, title = None, description = None, colour = None):
        self.title = title
        self.description = description
        self.embed = {
            "title": title,
            "description": description,
            "colour": colour
        }

    @property
    def get_embed(self):
        return self.embed

    def add_field(self, name: str, value: str, inline: bool= False):
        field = {
            "name": name,
            "value": value,
            "inline": inline
        }
        try:
            self.embed["fields"].append(field)
        except:
            self.embed["fields"] = [field]

    def set_footer(self, text: str, icon_url: str = None):
        footer = {
            "text": text,
            "icon_url": icon_url
        }
        self.embed["footer"] = footer