from brown.utils.units import Unit


class Point:
    """An (x, y) point with a page number"""

    __slots__ = ('_x', '_y', '_page')

    def __init__(self, x, y, page=0):
        """
        Args:
            x (float or Unit): The x axis position
            y (float or Unit): The y axis position
            page (int): The page number.
        """
        self._x = x
        self._y = y
        self._page = page

    ######## PUBLIC CLASS METHODS ########

    @classmethod
    def from_existing(cls, point):
        """Clone a Point

        Args:
            point (Point): The point to clone

        Returns: Point
        """
        return cls(point.x, point.y, point.page)

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

    @property
    def page(self):
        """int: The page number of the point.

        Note that, like the `x` and `y` properties, the page number
        is a *relative* value. As a result, `page=0` relative to the
        document root actually means the first printed page.
        """
        return self._page

    @page.setter
    def page(self, value):
        self._page = value

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
        return '{}({}, {}, {})'.format(type(self).__name__,
                                       self.x,
                                       self.y,
                                       self.page)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        """Two Points are equal if their attributes are all equal.

        Returns: Bool
        """
        if isinstance(other, type(self)):
            return (self.x == other.x and
                    self.y == other.y and
                    self.page == other.page)
        else:
            return False

    def __add__(self, other):
        """`Point`s are added by adding their x and y values in a new `Point`

        Returns: Point
        """
        if not isinstance(other, type(self)):
            raise TypeError('Cannot add "{}" and "{}"'.format(
                type(self).__name__, type(other).__name__))
        return type(self)(self.x + other.x,
                          self.y + other.y,
                          self.page + other.page)

    def __sub__(self, other):
        """`Point`s are subtracted by adding their x and y values in a new `Point`

        Returns: Point
        """
        if not isinstance(other, type(self)):
            raise TypeError('Cannot subtract "{}" and "{}"'.format(
                type(self).__name__, type(other).__name__))
        return type(self)(self.x - other.x,
                          self.y - other.y,
                          self.page - other.page)

    def __mul__(self, other):
        """Points may be multiplied with scalars.

        Args:
            other (Unit, int, float): A scalar value

        Returns: Point

        The resulting Point's page number will always be the same as the original.
        """
        if not isinstance(other, (Unit, int, float)):
            raise TypeError('Cannot multiply "{}" and "{}"'.format(
                type(self).__name__, type(other).__name__))
        return type(self)(self.x * other, self.y * other, self.page)

    def __abs__(self):
        # TODO: Evaluate if this is needed (probably not!)
        return type(self)(abs(self.x), abs(self.y), abs(self.page))

    def __round__(self, ndigits=None):
        return type(self)(round(self.x, ndigits),
                          round(self.y, ndigits),
                          self.page)
