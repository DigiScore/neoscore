from enum import Enum


class FillPattern(Enum):

    """An enumeration of pen stroke patterns.

    Only the below enumerated patterns are currently supported,
    but if needed it is possible to implement gradient patterns
    and arbitrary custom patterns. See the following page from
    the relevant Qt docs:
        https://doc.qt.io/qt-5/qt.html#BrushStyle-enum
    """
    # No brush pattern. This is equivalent to a fully transparent color.
    NO_BRUSH = 0
    # Uniform solid color.
    SOLID = 1
    # Extremely dense brush pattern.
    DENSE_1 = 2
    # Very dense brush pattern.
    DENSE_2 = 3
    # Somewhat dense brush pattern.
    DENSE_3 = 4
    # Half dense brush pattern.
    DENSE_4 = 5
    # Somewhat sparse brush pattern.
    DENSE_5 = 6
    # Very sparse brush pattern.
    DENSE_6 = 7
    # Extremely sparse brush pattern.
    DENSE_7 = 8
    # Horizontal lines.
    HORIZONTAL_LINES = 9
    # Vertical lines.
    VERTICAL_LINES = 10
    # Crossing horizontal and vertical lines.
    CROSSING_VERTICAL_HORIZONTAL_LINES = 11
    # Diagonal lines ascending from left to right.
    ASCENDING_DIAGONAL_LINES = 12
    # Diagonal lines descending from left to right.
    DESCENDING_DIAGONAL_LINES = 13
    # Crossing diagonal lines.
    CROSSING_DIAGIONAL_LINES = 14
