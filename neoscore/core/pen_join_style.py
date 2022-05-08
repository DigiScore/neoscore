from enum import Enum


class PenJoinStyle(Enum):

    """Styles controlling the shape of line joints on a pen stroke.

    The enum int values are for internal purposes and not guaranteed by the API.
    """

    # Values align with Qt's http://doc.qt.io/qt-5.9/qt.html#PenJoinStyle-enum

    BEVEL = 0x40
    """The triangular notch between the two lines is filled."""

    MITER = 0x00
    """The outer edges of the lines are extended to meet at an angle."""

    ROUND = 0x80
    """A circular arc between the two lines is filled."""
