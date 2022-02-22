from typing import Union

from brown.utils.units import GraphicUnit, Unit


class Point:
    """A two dimensional point.

    The x-axis grows left-to right, and the y-axis grows top-to-bottom.
    """

    __slots__ = ("_x", "_y")

    def __init__(self, x: Unit, y: Unit):
        """
        Args:
            x: The x axis position
            y: The y axis position
        """
        self._x = x
        self._y = y

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self) -> Unit:
        """Unit, int, or float: The x coordinate of the point."""
        return self._x

    @property
    def y(self) -> Unit:
        """Unit, int, or float: The y coordinate of the point."""
        return self._y

    ######## SPECIAL METHODS ########

    def __repr__(self):
        return "{}({}, {})".format(type(self).__name__, self.x, self.y)

    def __hash__(self):
        return 23984743 ^ hash(self.x) ^ hash(self.y)

    def __eq__(self, other):
        """Two Points are equal if their attributes are all equal.

        Returns: Bool
        """
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __add__(self, other):
        """`Point`s are added by adding their x and y values in a new `Point`

        Returns: Point
        """
        if type(other) != type(self):
            raise TypeError
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """`Point`s are subtracted by adding their x and y values in a new `Point`

        Returns: Point
        """
        if type(other) != type(self):
            raise TypeError
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Points may be multiplied with scalars.

        Args:
            other (Unit, int, float): A scalar value

        Returns: Point
        """
        if not isinstance(other, (Unit, int, float)):
            raise TypeError
        return type(self)(self.x * other, self.y * other)

    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y))
