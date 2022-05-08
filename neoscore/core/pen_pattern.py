from enum import Enum


class PenPattern(Enum):

    """Pen stroke patterns.

    The enum int values are for internal purposes and not guaranteed by the API.
    """

    # These values align with Qt's values http://doc.qt.io/qt-5.7/qt.html#PenStyle-enum

    INVISIBLE = 0
    """No pen pattern. This is equivalent to a fully transparent color.

    Instead of using this pattern directly, you may want to use :obj:`.Pen.no_pen()`
    instead.
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
