from .colour import Colour

class Embed:
    def __init__(self, title = None, description = None, colour = None):
        self.title = title
        self.description = description
        self.colour: hex = colour
        self.embed = {
            "title": title,
            "description": description,
            "colour": hex
        }

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