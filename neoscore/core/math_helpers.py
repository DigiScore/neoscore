"""General math helper tools."""

import math

from neoscore.core.point import Point
from neoscore.core.units import Unit


def interpolate(line_start: Point, line_end: Point, x: Unit) -> Unit:
    """Calculate the value of a line defined by two points at a given x pos

    Args:
        line_start: The start of the line
        line_end: The end of the line
        x: The position to interpolate from

    Returns: Unit
    """
    slope = (line_end.y - line_start.y) / (line_end.x - line_start.x)
    y_intercept = line_start.y - (line_start.x * slope)
    return (x * slope) + y_intercept


def clamp_value(value, minimum, maximum):
    """Clamp a value to fit within a range.

    * If `value` is less than `minimum`, return `minimum`.
    * If `value` is greater than `maximum`, return `maximum`
    * Otherwise, return `value`

    Args:
        value (number or Unit): The value to clamp
        minimum (number or Unit): The lower bound
        maximum (number or Unit): The upper bound

    Returns:
        int or float: The clamped value

    Example:
        >>> clamp_value(-1, 2, 10)
        2
        >>> clamp_value(4.0, 2, 10)
        4.0
        >>> clamp_value(12, 2, 10)
        10
    """
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    else:
        return value


def min_and_max(iterable):
    """Efficiently get the min and max of an iterable

    Args:
        iterable (Iterable): An iterable whose elements can all be
            compared with each other

    Returns: tuple(min, max)
    """
    minimum = iterable[0]
    maximum = iterable[0]
    for value in iterable:
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value
    return minimum, maximum


def sign(value: Unit) -> int:
    """Return the sign of a unit as 1 or -1.

    Args:
        value: The value to check

    Returns: -1 if `value` is negative, and 1 if `value` is positive
    """
    if value.base_value < 0:
        return -1
    else:
        return 1


def is_power_of_2(value: int) -> bool:
    return (value & (value - 1) == 0) and value != 0


def point_angle(point: Point) -> float:
    """Calculate the angle from the positive X axis to a point in radians.

    The returned angle goes positive clockwise and is between pi and -pi.

    Combine with the Python stdlib function `math.degrees()` to get
    the angle in degrees.
    """
    return math.atan2(point.y.base_value, point.x.base_value)
