from enum import Enum


class StrokePattern(Enum):

    """An enumeration of pen stroke patterns.

    Only the below enumerated patterns are currently supported,
    but if needed it is possible to implement arbitrary custom
    patterns. See the following page from the relevant Qt docs:
        http://doc.qt.io/qt-5.7/qt.html#PenStyle-enum
    """

    # A solid line
    SOLID = 1

    # Dashes separated by blank space
    DASH = 2

    # Small dots separated by blank space
    DOT = 3

    # Alternating dashes and dots
    DASHDOT = 4

    # A repeating pattern of one dash and two dots
    DASHDOTDOT = 5
