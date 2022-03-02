import io
import os
from typing import TYPE_CHECKING, Optional, Union

__all__ = ("File",)


class File:

    __slots__ = ("fp", "filename", "spoiler", "_close", "_is_owner")

    if TYPE_CHECKING:
        fp: io.BufferedIOBase
        filename: Optional[str]
        spoiler: bool

    def __init__(
        self,
        fp: Union[str, bytes, os.PathLike, io.BufferedIOBase],
        *,
        filename: Optional[str] = None,
        spoiler: bool = False
    ):
        if isinstance(fp, io.IOBase):
            self.fp = fp
            self._is_owner = False
        else:
            self.fp = open(fp, "rb")
            self._is_owner = True

        self._close = self.fp.close
        self.fp.close = lambda: None

        if not filename:
            if isinstance(filename, str):
                self.filename = os.path.split[0]
            else:
                self.filename = getattr(fp, "name", None)
        else:
            self.filename = filename

    def close(self) -> None:
        self.fp.close = self._close
        if self._is_owner:
            return self._close()
