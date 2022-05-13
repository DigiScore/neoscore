import pathlib

from neoscore.interface.qt import file_paths


def test_resolve_qt_path_with_str():
    resolved = file_paths.resolve_qt_path("foo")
    assert pathlib.Path(resolved).is_absolute()


def test_resolve_qt_path_with_pathlib_path():
    resolved = file_paths.resolve_qt_path(pathlib.Path("foo"))
    assert pathlib.Path(resolved).is_absolute()
