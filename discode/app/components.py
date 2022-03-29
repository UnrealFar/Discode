from __future__ import annotations

__all__ = (
    "Button",
    "LinkButton",
    "URLButton",
    "component_from_dict",
)

import asyncio
import os
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Optional, Union

from ..enums import ButtonStyle
from ..utils import UNDEFINED


class Button:

    __slots__ = (
        "type",
        "style",
        "label",
        "custom_id",
        "callback",
        "disabled",
    )

    if TYPE_CHECKING:
        type: int
        style: int
        label: str
        custom_id: Optional[str]
        disabled: bool
        callback: Awaitable[Any]

    def __init__(
        self,
        *,
        label: Optional[str] = UNDEFINED,
        style: Optional[Union[ButtonStyle, int]] = UNDEFINED,
        custom_id: Optional[str] = UNDEFINED,
        callback: Optional[Callable[Any]] = UNDEFINED,
        disabled: bool = False,
    ):
        if custom_id == UNDEFINED:
            custom_id = os.urandom(16).hex()
        if (not asyncio.iscoroutinefunction(callback)):
            if callback != UNDEFINED:
                raise TypeError("Button callback can only be a coroutine.")
            callback = lambda interaction: None
            callback = asyncio.coroutine(callback)
        setattr(self, "callback", callback)
        self.type = 2
        self.label = label if label else None
        self.custom_id = custom_id
        self.disabled = disabled
        if style == ButtonStyle.link:
            raise ValueError(
                "URL/link buttons should be subclassed from class discode.models.components.LinkButton"
            )
        self.style = int(style) if style != UNDEFINED else ButtonStyle.primary

    def __bool__(self) -> bool:
        return not self.disabled

    @classmethod
    def from_dict(cls: Button, payload: Dict[str, Any]):
        button = cls(
            label=payload.get("label", UNDEFINED),
            style=payload.get("style", UNDEFINED),
            custom_id=payload.get("custom_id", UNDEFINED),
            disabled=payload.get("disabled", False),
        )
        return button


class LinkButton(Button):

    __slots__ = ("type", "style", "label", "url")

    if TYPE_CHECKING:
        type: int
        style: int
        label: str
        url: str

    def __init__(
        self,
        *,
        label: Optional[str] = UNDEFINED,
        url: str = UNDEFINED,
    ):
        self.type = 2
        self.style = ButtonStyle.link
        self.label = label if label else None
        self.url = str(url)

    @classmethod
    def from_dict(cls: LinkButton, payload: Dict[str, Any]):
        button = cls(
            label=payload.get("label", UNDEFINED), url=payload.get("url", UNDEFINED)
        )
        return button


URLButton = LinkButton


def component_from_dict(payload: Dict[str, Any]):
    if payload.get("type") == 2:
        if payload.get("style") == ButtonStyle.link:
            return LinkButton.from_dict(payload)
        return Button.from_dict(payload)
