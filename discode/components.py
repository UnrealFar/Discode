from typing import Optional, Union, Any, List
import os

from .styles import ButtonStyle

class Component:
    r"""Represnts a Discord component.
    Can be either a :class:`Button` or a :class:`SelectMenu`.
    """
    def __init__(
        self,
        *args,
        **kwargs
    ):
        pass

class Button(Component):
    r"""Represents a Discord Button.

    Parameters
    ----------

    style: Union[:class:`ButtonStyle`, int] = :class:`ButtonStyle.primary`
        The style of the button. This should be empty if the button is a url button.

    label: Optional[str] = None
        The label of the button.

    disabled: bool = False
        Whether to make the button disabled or not.

    custom_id: Optional[str] = None
        The custom id of the button. Specify this if you want to make the button persistent.

    row: ActionRow
        The :class:`ActionRow` to which the button belongs.
    """
    def __init__(
        self,
        style: Union[ButtonStyle, int] = ButtonStyle.primary,
        label: Optional[str] = None,
        disabled: bool = False,
        custom_id: Any = None,
        url: Optional[str] = None,
        row: "ActionRow" = None,
        *args,
        **kwargs
    ):
        super().__init__()
        self.style = style

        if url and custom_id:
            raise TypeError("Cannot use custom_id field in a url style button!")

        if style == ButtonStyle.url and not url:
            raise TypeError("ButtonStyle.url can only be used if a url is specified.")

        if url:
            self.style = ButtonStyle.url
            self.url = url

        if not url:
            if custom_id:
                self.custom_id = custom_id
            else:
                self.custom_id = os.urandom(16).hex()

        self.label = label
        self.disabled: bool = disabled
        self.row: "ActionRow" = row

    def get_payload(self):
        data = {
            "type": 2,
            "style": self.style
        }
        if hasattr(self, "url"):
            data["url"] = self.url
            if self.label:
                data["label"] = self.label
            return data

        data["custom_id"] = self.custom_id

        if self.label:
            data["label"] = self.label

        return data

    @classmethod
    def from_json(cls: ..., data: dict) -> ...:
        data.pop("type", None)
        return cls(**data)

class ActionRow(Component):
    def __init__(
        self,
        *args
    ):

        self.items: List[Union[Component, Button]] = []

    @classmethod
    def from_json(cls: "ActionRow", data: dict) -> "ActionRow":
        ar = cls()
        for comp in data.get("components"):
            if isinstance(comp, dict):
                if comp.get("type") == 2:
                    comp = Button.from_json(comp)

            ar.items.append(comp)

        return ar

    def get_payload(self) -> dict:
        data = {}

        data["components"] = []
        data["type"] = 1

        for item in self.items:
            data["components"].append(item.get_payload())

        return data
