"""General math helper tools."""

import math
from typing import Tuple

from neoscore.core.point import Point
from neoscore.core.units import Unit


def interpolate(line_start: Point, line_end: Point, x: Unit) -> Unit:
    """Calculate the value of a line defined by two points at a given x pos."""
    slope = (line_end.y - line_start.y) / (line_end.x - line_start.x)
    y_intercept = line_start.y - (line_start.x * slope)
    return (x * slope) + y_intercept


def is_power_of_2(value: int) -> bool:
    """Check if a number is a power of 2."""
    return (value & (value - 1) == 0) and value != 0


def point_angle(point: Point) -> float:
    """Calculate the angle from the positive X axis to a point in radians.

    The returned angle goes positive clockwise and is between pi and -pi.

    Combine with the Python stdlib function ``math.degrees()`` to get
    the angle in degrees.
    """
    return math.atan2(point.y.base_value, point.x.base_value)


def dist(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Find the Euclidean distance between two 2D float tuples.

    In the future this function and signature may be modified to support neoscore
    unit-points as well.
    """
    return math.sqrt(((p2[1] - p1[1]) ** 2) + ((p2[0] - p1[0]) ** 2))
