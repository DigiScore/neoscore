import os
import pathlib
from typing import Union


def resolve_qt_path(path: Union[str, pathlib.Path]) -> str:
    """Convert a path to a string compatible with Qt's path-using methods."""
    if isinstance(path, str):
        path = pathlib.Path(path)
    return os.path.abspath(path)
