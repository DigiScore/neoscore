import sys

from enum import Enum, auto


class PlatformType(Enum):
    """Common operating systems"""

    bsd = auto()
    linux = auto()
    mac = auto()
    windows = auto()
    unknown = auto()


def current_platform():
    """Get the type of the running platform"""
    if sys.platform.startswith('freebsd'):
        return PlatformType.bsd
    elif sys.platform.startswith('linux'):
        return PlatformType.linux
    elif sys.platform == 'darwin':
        return PlatformType.mac
    elif sys.platform == 'win32' or sys.platform == 'cygwin':
        return PlatformType.windows
    return PlatformType.unkown
