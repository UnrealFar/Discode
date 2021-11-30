from typing import Union, Callable, List

from .client import Client


class Bot(Client):
    def __init__(
        self,
        prefix: Union[str, Callable, List],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.prefix = prefix

        # TODO add commands and application cmds
