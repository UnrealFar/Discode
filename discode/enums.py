from enum import IntEnum

class ButtonStyle(IntEnum):
    r"""Represents the style of a :class:`Button`."""
    primary = 1
    secondary = 2
    success = 3
    danger = 4
    url = 5
    blurple = primary
    grey = secondary
    green = success
    red = danger
    link = url
