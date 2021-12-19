from typing import Union, Optional, List

from .colours import Colour, Color

class Embed:
    r"""Represents a Discord embed. This part of a :class:`Message`.

    Attributes
    ----------
    title: Optional[str]
        The title of the embed.

    description: Optional[str] = None
        The description of the embed.

    colour: Optional[Union[:class:`Colour`, hex, int]] = None
        The colour of the embed.

    color: Optional[Union[:class:`Colour`, hex, int]] = colour
        The colour of the embed.

    fields: List[dict]
        The list of all the fields of the embed.

    
    """

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        colour: Optional[Union[Colour, Color, hex, int]] = None
    ):
        self.title: str = title
        self.description: str = description
        if isinstance(colour, Colour):
            self.colour = self.color= colour.value
        else:
            self.colour = self.color = colour

        self.fields: List[dict] = []
        self.footer: dict = None

    def add_field(self, name: str, value: str, inline: bool = True) -> "Embed":
        r"""Add a field to the embed object.

        Returns
        --------
        :class:`Embed`
            The embed object to which the field was added to.
        """
        self.fields.append(
            {
                "name": str(name),
                "value": str(value),
                "inline": inline
            }
        )
        return self

    def set_footer(self, text: str = None, icon_url: str = None) -> "Embed":
        r"""Set a footer for the embed.

        Returns
        --------
        :class:`Embed`
            The embed to which the field was added to.
        """
        data = {}
        if text:
            data["text"] = str(text)
        if icon_url:
            data["icon_url"] = str(icon_url)
        self.footer = data
        return self

    def get_payload(self) -> dict:
        data = {}
        if self.title:
            data["title"] = self.title
        if self.description:
            data["description"] = self.description

        if self.colour:
            data["color"] = self.colour

        if len(self.fields) > 0:
            data["fields"] = self.fields

        if self.footer:
            data["footer"] = self.footer

        return data

    @classmethod
    def from_json(cls: "Embed", data: dict) -> "Embed":
        emb: "Embed" = cls(
            title = data.pop("title", None),
            description = data.pop("description", None),
            colour = data.pop("color", None)
        )

        if "fields" in data:
            for field in data.pop("fields", []):
                emb.add_field(
                    name = field.pop("name", None),
                    value = field.pop("value", None),
                    inline = data.pop("inline", True)
                )

        if "footer" in data:
            emb.set_footer(
                text = data.pop("text", None),
                icon_url = data.pop("icon_url", None)
            )

        return emb
