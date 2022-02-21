from typing import Union

from brown.utils.units import GraphicUnit, Unit

# TODO pretty sure this should be made immutable


class Point:
    """A two dimensional point.

    The x-axis grows left-to right, and the y-axis grows top-to-bottom.
    """

    __slots__ = ("_x", "_y")

    def __init__(self, x: Union[Unit, float], y: Union[Unit, float]):
        """
        Args:
            x (float or Unit): The x axis position
            y (float or Unit): The y axis position
        """
        self._x = x if isinstance(x, Unit) else GraphicUnit(x)
        self._y = y if isinstance(y, Unit) else GraphicUnit(y)

    ######## PUBLIC CLASS METHODS ########

    @classmethod
    def from_existing(cls, point):
        """Clone a Point

        Args:
            point (Point): The point to clone

        Returns: Point
        """
        return cls(point.x, point.y)

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self) -> Unit:
        """Unit, int, or float: The x coordinate of the point."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value if isinstance(value, Unit) else GraphicUnit(value)

    @property
    def y(self) -> Unit:
        """Unit, int, or float: The y coordinate of the point."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value if isinstance(value, Unit) else GraphicUnit(value)

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
