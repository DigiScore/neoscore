from enum import Enum


class PenPattern(Enum):

    """An enumeration of pen stroke patterns.

    Only the below enumerated patterns are currently supported,
    but if needed it is possible to implement arbitrary custom
    patterns. See the following page from the relevant Qt docs:
        http://doc.qt.io/qt-5.7/qt.html#PenStyle-enum
    """
    SOLID = 1
    """A solid line"""

    DASH = 2
    """Dashes separated by blank space"""

    DOT = 3
    """Small dots separated by blank space"""

    DASHDOT = 4
    """Alternating dashes and dots"""

    DASHDOTDOT = 5
    """A repeating pattern of one dash and two dots"""
