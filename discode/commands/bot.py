from typing import Union, Callable, List

from discode import Client

__all__ = ("Bot",)

class Bot(Client):
    r"""Represents the bot that connects to Discord.

    Parameters
    -----------
    """

    def __init__(
        self,
        **kwargs
    ):
        super().__init__(**kwargs)

        # TODO add commands and application cmds
