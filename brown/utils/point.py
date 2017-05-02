from brown.utils.units import Unit


class Point:
    """A two dimensional point.

    The x-axis grows left-to right, and the y-axis grows top-to-bottom.
    """

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

    @classmethod
    def from_parent_point(cls, parent_point):
        """Create a Point from an ParentPoint, discarding its parent.

        Args:
            parent_point (ParentPoint):

        Returns: Point
        """
        return cls(parent_point.x, parent_point.y)

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
        return '{}({}, {})'.format(type(self).__name__,
                                   self.x,
                                   self.y)

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
        if type(other) != type(self):
            raise TypeError
        return type(self)(self.x + other.x,
                          self.y + other.y)

    def __sub__(self, other):
        """`Point`s are subtracted by adding their x and y values in a new `Point`

        Returns: Point
        """
        if type(other) != type(self):
            raise TypeError
        return type(self)(self.x - other.x,
                          self.y - other.y)

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

    def __round__(self, ndigits=None):
        return type(self)(round(self.x, ndigits),
                          round(self.y, ndigits))

    ######### PRIVATE METHODS ########

    def _assert_almost_equal(self, other, places=7):
        """Assert the near-equality of two points.

        **For testing purposes only.**

        Both `self.x` and `self.y` must be `Unit`types.
        """
        self.x._assert_almost_equal(other.x)
        self.y._assert_almost_equal(other.y)