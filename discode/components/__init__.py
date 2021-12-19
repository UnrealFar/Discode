from typing import Optional, Union
import os

from discode.enums import ButtonStyle

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

    row: Optional[int]
        The action row to which the button belongs.
    """
    def __init__(
        self,
        style: Union[ButtonStyle, int] = ButtonStyle.primary,
        label: Optional[str] = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        url: Optional[str] = None,
        row: Optional[int] = None
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

        else:
            if not self.style == ButtonStyle.url:
                if label is None or label == "":
                    raise TypeError("Label cannot be empty in a non-url button!")

        if not url:
            if custom_id:
                self.custom_id = custom_id
            else:
                self.custom_id = os.urandom(16).hex()

        self.disabled = disabled

    def get_payload(self):
        data = {
            "type": 2,
            "style": self.style
        }
        if self.url:
            data["url"] = self.url
            return data

        data["custom_id"] = self.custom_id

        if self.label:
            data["label"] = self.label

        return data

    @classmethod
    def from_json(cls: ..., data: dict) -> ...:
        data.pop("type", None)
        return cls(**data)
