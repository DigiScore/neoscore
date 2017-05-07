from enum import Enum


class BrushPattern(Enum):

    """An enumeration of pen stroke patterns.

    Only the below enumerated patterns are currently supported,
    but if needed it is possible to implement gradient patterns
    and arbitrary custom patterns. See the following page from
    the relevant Qt docs:
        https://doc.qt.io/qt-5/qt.html#BrushStyle-enum
    """
    NO_BRUSH = 0
    """No brush pattern. This is equivalent to a fully transparent color."""

    SOLID = 1
    """Uniform solid color."""

    DENSE_1 = 2
    """Extremely dense brush pattern."""

    DENSE_2 = 3
    """Very dense brush pattern."""

    DENSE_3 = 4
    """Somewhat dense brush pattern."""

    DENSE_4 = 5
    """Half dense brush pattern."""

    DENSE_5 = 6
    """Somewhat sparse brush pattern."""

    DENSE_6 = 7
    """Very sparse brush pattern."""

    DENSE_7 = 8
    """Extremely sparse brush pattern."""

    HORIZONTAL_LINES = 9
    """Horizontal lines."""

    VERTICAL_LINES = 10
    """Vertical lines."""

    CROSSING_VERTICAL_HORIZONTAL_LINES = 11
    """Crossing horizontal and vertical lines."""

    ASCENDING_DIAGONAL_LINES = 12
    """Diagonal lines ascending from left to right."""

    DESCENDING_DIAGONAL_LINES = 13
    """Diagonal lines descending from left to right."""

    CROSSING_DIAGONAL_LINES = 14
    """Crossing diagonal lines."""
