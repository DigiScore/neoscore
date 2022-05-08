from enum import Enum


class PenCapStyle(Enum):

    """Styles controlling how pen strokes are capped.

    The enum int values are for internal purposes and not guaranteed by the API.
    """

    # Values align with Qt's http://doc.qt.io/qt-5.9/qt.html#PenCapStyle-enum

    SQUARE = 0x10
    """A square cap that extends beyond the end point by half the pen width"""

    FLAT = 0x00
    """A square cap that does not cover the end point of the path"""

    ROUND = 0x20
    """A rounded cap"""
