from __future__ import annotations

from typing import NamedTuple

from brown.utils.units import GraphicUnit, Unit


class Point(NamedTuple):
    """A two dimensional point.

    The x-axis grows left-to right, and the y-axis grows top-to-bottom.
    """

    x: Unit
    y: Unit

    ######## SPECIAL METHODS ########

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
