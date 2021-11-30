from typing import Union, Optional

from .color import Colour

class Embed:
    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        colour: Union[Colour, hex, int] = None
    ):
        self.data = data = {}
        if title:
            data["title"] = self.title = str(title)
        if description:
            data["description"] = self.description = str(description)
        if colour:
            data["colour"] = self.colour = getattr(colour, "value", colour)

        data["fields"] = []

    def add_field(self, name: str, value: str, inline: bool = True):
        self.data["fields"].append(
            {
                "name": str(name),
                "value": str(value),
                "inline": inline
            }
        )
        return self

    def set_footer(self, text: str = None, icon_url: str = None):
        data = {}
        if text:
            data["text"] = str(text)
        if icon_url:
            data["icon_url"] = str(icon_url)
        self.data["footer"] = data
        return self
