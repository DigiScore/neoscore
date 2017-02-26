from brown.utils.units import Unit


class Point:
    """A 2D point."""

    __slots__ = ('_x', '_y')

    def __init__(self, x, y):
        """
        Args:
            x (float or Unit): The x axis position
            y (float or Unit): The y axis position
        """
        self._x = x
        self._y = y

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
    def x(self):
        """Unit, int, or float: The x coordinate of the point."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Unit, int, or float: The y coordinate of the point."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    ######## PUBLIC METHODS ########

    def to_unit(self, unit):
        """Translate coordinates to be of a certain unit type.

        Args:
            unit (type): A Unit class.

        Returns:
            Point: the modified self point.
        """
        self.x = unit(self.x)
        self.y = unit(self.y)
        return self

    ######## SPECIAL METHODS ########

    def __repr__(self):
        return '{}({}, {})'.format(type(self).__name__, self.x, self.y)

    def __hash__(self):
        return hash(self.__repr__())

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
        if not isinstance(other, type(self)):
            raise TypeError('Cannot add "{}" and "{}"'.format(
                type(self).__name__, type(other).__name__))
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """`Point`s are subtracted by adding their x and y values in a new `Point`

        Returns: Point
        """
        if not isinstance(other, type(self)):
            raise TypeError('Cannot subtract "{}" and "{}"'.format(
                type(self).__name__, type(other).__name__))
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """`Point`s may be multiplied with scalars to return transformed `Point`s

        Returns: Point
        """
        if not isinstance(other, (Unit, int, float)):
            raise TypeError('Cannot multiply "{}" and "{}"'.format(
                type(self).__name__, type(other).__name__))
        return type(self)(self.x * other, self.y * other)

    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y))

    def __round__(self, ndigits=None):
        return type(self)(round(self.x, ndigits), round(self.y, ndigits))
