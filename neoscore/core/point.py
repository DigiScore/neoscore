from __future__ import annotations

from typing import NamedTuple, Tuple, Union, cast

from typing_extensions import TypeAlias

from neoscore.core.units import ZERO, Unit


class Point(NamedTuple):
    """A two-dimensional point.

    The x-axis grows left-to right, and the y-axis grows top-to-bottom.
    """

    x: Unit
    """The horizontal X-axis value"""

    y: Unit
    """The vertical Y-axis value"""

    @staticmethod
    def from_def(point_def: PointDef) -> Point:
        if hasattr(point_def, "x"):
            return cast(Point, point_def)
        return Point(*point_def)

    def __add__(self, other: Point) -> Point:
        """Points are added by adding their x and y values respectively"""
        try:
            return Point(self.x + other.x, self.y + other.y)
        except AttributeError:
            raise TypeError

    def __sub__(self, other: Point) -> Point:
        """Points are subtracted by subtracting their x and y values respectively"""
        try:
            return Point(self.x - other.x, self.y - other.y)
        except AttributeError:
            raise TypeError

    def __mul__(self, other: float) -> Point:
        """Points may be multiplied by non-unit scalars.

        This is done by multiplying the x and y values by that scalar.
        """
        try:
            return Point(self.x * other, self.y * other)
        except AttributeError:
            raise TypeError

    def __abs__(self) -> Point:
        """Get a Point whose x and y values are the absolute values of this point's."""
        return Point(abs(self.x), abs(self.y))

    def __neg__(self) -> Point:
        """Get a Point whose x and y values are the negation of this point's."""
        return Point(-self.x, -self.y)


ORIGIN = Point(ZERO, ZERO)
"""Shorthand for a point at ``ZERO, ZERO``"""

PointDef: TypeAlias = Union[Point, Tuple[Unit, Unit]]
"""A Point or an argument tuple for one"""
