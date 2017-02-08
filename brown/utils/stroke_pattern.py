from enum import Enum


class StrokePattern(Enum):

    """An enumeration of pen stroke patterns."""

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
