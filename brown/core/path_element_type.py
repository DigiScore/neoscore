from enum import Enum


class PathElementType(Enum):
    """Enum for types of path elements"""

    move_to = 0
    """Moving directly to a new position without drawing a line to it."""

    line_to = 1
    """Drawing a line to a new position."""

    curve_to = 2
    """The ending location of a bezier curve."""

    control_point = 3
    """A control point in a bezier curve.

    This alone does not draw a curve - a series of these must occur
    before a `curve_to` element completes it.
    """
