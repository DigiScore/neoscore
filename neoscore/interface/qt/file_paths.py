import pathlib


def resolve_qt_path(path: str | pathlib.Path) -> str:
    """Convert a path to a string compatible with Qt's path-using methods."""
    if isinstance(path, str):
        path = pathlib.Path(path)
    path = path.resolve()
    return str(path)
