from typing import Optional
import os

from .enums import ButtonStyle

class Component:
    r"""Represnts a Discord component.
    Can be either a :class:`Button` or a :class:`SelectMenu`.
    """
    def __init__(
        self
    ):
        self.data = {}

class Button(Component):
    r"""Represents a Discord Button.
    """
    def __init__(
        self,
        *,
        style: ButtonStyle = ButtonStyle.primary,
        label: Optional[str] = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        url: Optional[str] = None,
        emoji: str = None
    ):
        super().__init__()
        if url and custom_id:
            raise TypeError("Cannot use custom_id field in a url styld button!")

        if url:
            style = ButtonStyle.url

        if not url:
            if custom_id:
                self.custom_id = custom_id
            else:
                self.custom_id = os.urandom(16).hex()
