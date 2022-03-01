
from __future__ import annotations

from typing import (
    Optional,
    Union,
    Any,
    Dict,
    List,
    TYPE_CHECKING
)

class Embed:
    r"""Represents a Discord Embed.

    Attrbutes
    ----------

    title: str
        The title of the embed.
    description: str
        The description of the embed.
    colour: Union[hex, int]
        The colour of the embed. Can be of type :class:`int`, :class:`hex` or of :class:`Colour`
    
    """

    __slots__ = (
        "title",
        "description",
        "colour",
        "fields"
    )

    if TYPE_CHECKING:
        title: str
        description: str
        colour: Union[int, hex]
        fields: List[EmbedField]

    def __init__(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        colour: Union[hex, int] = None
    ):
        self.title = str(title) if title else None
        self.description = str(description) if description else None
        self.colour = int(colour) if colour else None
        self.fields = []

    def add_field(
        self,
        name: Optional[str],
        value: Optional[str]
    ):
        ret = EmbedField(name = name, value = value, embed = self)
        self.fields.append(ret)
        return ret

    def to_dict(self) -> Dict[str, Any]:
        ret = dict()
        if self.title:
            ret["title"] = self.title
        if self.description:
            ret["description"] = self.description
        if self.colour:
            ret["color"] = self.colour
        if len(self.fields) >= 1:
            ret["fields"] = [field.to_dict() for field in self.fields]

        return ret

class EmbedField:
    __slots__ = (
        "name",
        "value",
        "embed"
    )

    if TYPE_CHECKING:
        name: str
        value: str
        embed: Embed

    def __init__(self, name: str, value: str, embed: Embed):
        if not name or not value:
            raise ValueError("Name and Value of an embed field cannot be None")
        self.name = name
        self.value = value
        self.embed = embed

    def to_dict(self):
        return dict(name = self.name, value = self.value)
