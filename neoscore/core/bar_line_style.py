from enum import Enum


class BarLineStyle(Enum):

    """An enumeration of pen stroke patterns.

    Only the below enumerated patterns are currently supported,
    but if needed it is possible to implement gradient patterns
    and arbitrary custom patterns. See the following page from
    the relevant Qt docs:
        https://doc.qt.io/qt-5/qt.html#BrushStyle-enum

    The corresponding integer values must align with Qt's enum values.
    """

    SINGLE = 0
    """Single line style. Used for normal bar seperation."""

    THICK_DOUBLE = 1
    """Think double bar line. Used for end of score."""

    THIN_DOUBLE = 2
    """This double bar line. Used for section separation."""

    DASHED = 3
    """Dashed single bar line."""