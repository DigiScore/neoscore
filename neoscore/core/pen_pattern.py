from enum import Enum


class PenPattern(Enum):

    """Pen stroke patterns"""

    # These values align with Qt's values http://doc.qt.io/qt-5.7/qt.html#PenStyle-enum

    INVISIBLE = 0

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
