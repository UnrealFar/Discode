
from typing import (
    Optional,
    Any,
    Dict,
    List,
    TYPE_CHECKING
)

class Embed:
    r"""Represents a Discord Embed
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
        colour: int
        fields: List[Dict[str, Any]]

    def __init__(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        colour: hex = None
    ):
        self.title = str(title) if title else None
        self.desctiption = str(description) if description else None
        self.colour = int(colour) if colour else None

    def to_dict(self) -> Dict[str, Any]:
        ret = dict()
        if self.title:
            ret["title"] = self.title
        if self.description:
            ret["title"] = self.description
        if self.colour:
            ret["color"] = self.colour
