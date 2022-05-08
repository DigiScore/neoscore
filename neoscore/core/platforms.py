import sys
from enum import Enum, auto


class PlatformType(Enum):
    """Common operating systems"""

    BSD = auto()
    LINUX = auto()
    MAC = auto()
    WINDOWS = auto()
    UNKNOWN = auto()


def current_platform() -> PlatformType:
    """Get the type of the running platform"""
    if sys.platform.startswith("freebsd"):
        return PlatformType.BSD
    elif sys.platform.startswith("linux"):
        return PlatformType.LINUX
    elif sys.platform == "darwin":
        return PlatformType.MAC
    elif sys.platform == "win32" or sys.platform == "cygwin":
        return PlatformType.WINDOWS
    return PlatformType.unkown
