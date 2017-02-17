from brown.utils.units import Unit


class Point:
    """A simple 2-d point class.

    Its x and y values may be accessed by name, iteration, and indexing:

        >>> p = Point(5, 6)
        >>> p.x == p[0] == 5
        True
        >>> p.y == p[1] == 6
        True
        >>> x, y = p
        >>> x
        5
        >>> y
        6

    """
    def __init__(self, x, y):
        """
        Args:
            x (float or Unit): The x axis position
            y (float or Unit): The y axis position
        """
        self._x = x
        self._y = y
        self._iter_index = 0

    ######## PRIVATE CLASS METHODS ########

    @classmethod
    def with_unit(cls, x, y, unit):
        """Create a Point and ensure its coordinates are in a type of unit.

        Args:
            x (float or Unit): The x axis position
            y (float or Unit): The y axis position
            unit (type): A Unit class.

        Returns: Point

        Example:
            >>> from brown.utils.units import Inch
            >>> p = Point.with_unit(2, 3, unit=Inch)
            >>> print(p.x)
            Inch(2)
            >>> print(p.y)
            Inch(3)

        TODO: Replace this method with the pattern:

                  Point(x, y).to_unit()

              and make to_unit() return the point (instead of None)
        """
        point = cls(x, y)
        point.to_unit(unit)
        return point

    @classmethod
    def from_existing(cls, point):
        """Create a point from an existing one, cloning its properties.

        Args:
            point (Point): The point to clone
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
        self.setters_hook()

    @property
    def y(self):
        """Unit, int, or float: The y coordinate of the point."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.setters_hook()

    ######## PUBLIC METHODS ########

    def to_unit(self, unit):
        """Translate coordinates to be of a certain unit type.

        Args:
            unit (type): A Unit class.

        Returns: None
        """
        self.x = unit(self.x)
        self.y = unit(self.y)

    def setters_hook(self):
        """Optional method to be called when an attribute changes.

        To set a change hook, instantiate a Point and set its `setters_hook`
        method to some arbitrary function. Any time an attribute is changed,
        this function will be called.

        Example:
            >>> class PointHolder:
            ...     def __init__(self):
            ...         self.point_setter_hook_called = False
            ...         self.point = Point(0, 0)
            ...         self.point.setters_hook = self.handle_hook
            ...
            ...     def handle_hook(self):
            ...         self.point_setter_hook_called = True
            >>> test_instance = PointHolder()
            >>> test_instance.point.x = 1  # Change x, triggering hook
            >>> test_instance.point_setter_hook_called
            True
        """
        pass

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

    def __iter__(self):
        return self

    def __getitem__(self, key):
        """Index into a Point, where 0 is x and 1 is y.

        Args:
            key (int): The indexing key

        Raises:
            TypeError: For all non-int `key` values
            IndexError: For all int `key` values other than `0` and `1`

        QUESTION: Should negative indexing be supported? Might be confusing.
        """
        if not isinstance(key, int):
            raise TypeError('Point keys must be of type `int`.')
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError('Only valid indices for {} '
                             'are 0 and 1 (Got {})'.format(
                                 type(self).__name__, key))

    def __next__(self):
        """Support iteration over a Point for indices 0 and 1."""
        if self._iter_index > 1:
            self._iter_index = 0
            raise StopIteration
        self._iter_index += 1
        if self._iter_index == 1:
            return self.x
        else:
            return self.y
