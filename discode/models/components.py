
from __future__ import annotations

from typing import (
    Optional,
    Union,
    Callable,
    TYPE_CHECKING,
)

import os
import asyncio

from ..utils import UNDEFINED
from ..enums import ButtonStyle

class Button:

    if TYPE_CHECKING:
        type: int
        style: int
        label: str
        custom_id: Optional[str]
        disabled: bool

    def __init__(
        self,
        *,
        label: Optional[str] = UNDEFINED,
        style: Optional[Union[ButtonStyle, int]] = UNDEFINED,
        custom_id: Optional[str] = UNDEFINED,
        callback: Optional[Callable] = UNDEFINED,
        disabled: bool = False,
    ):
        if custom_id == UNDEFINED:
            custom_id = os.urandom(16).hex()
        if not asyncio.iscoroutinefunction(callback):
            if callback != UNDEFINED:
                raise TypeError("Button callback can only be a coroutine.")
            else:
                setattr(self, "callback", callback)
        self.type = 2
        self.label = label if label else None
        self.custom_id = custom_id
        self.disabled = disabled
        if style == ButtonStyle.link:
            raise ValueError("URL/link buttons should be subclassed from class discode.models.components.LinkButton")
        self.style = int(style) if style != UNDEFINED else ButtonStyle.primary

    async def _call(self, *args, **kwargs) -> None:
        if hasattr(self, "callback"):
            await self.callback()

class LinkButton(Button):

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

URLButton = LinkButton
