from collections import namedtuple


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
    def __init__(self, *args):
        """
        *args: One of:
            - An `x, y` pair outside of a tuple
            - An `(x, y)` 2-tuple
            - An existing Point
        """
        if len(args) == 2:
            self.x, self.y = args
        elif len(args) == 1:
            if isinstance(args[0], tuple):
                self.x, self.y = args[0]
            elif isinstance(args[0], Point):
                self.x = args[0].x
                self.y = args[0].y
            else:
                raise ValueError('Invalid args for Point.__init__()')
        else:
            raise ValueError('Invalid args for Point.__init__()')

        self._iter_index = 0

    ######## PUBLIC METHODS ########

    def to_unit(self, unit_class):
        """Translate coordinates to be of a certain unit type.

        Args:
            unit_class (type): A BaseUnit class.

        Returns: None
        """
        self.x = unit_class(self.x)
        self.y = unit_class(self.y)

    ######## SPECIAL METHODS ########

    def __iter__(self):
        return self

    def __getitem__(self, key):
        """Index into a Point, where 0 is x and 1 is y.

        Args:
            key (int): The indexing key

        Raises:
            TypeError: For all non-int `key` values
            IndexError: For all int `key` values other than `0` and `1`
        """
        if not isinstance(key, int):
            raise TypeError('Point keys must be of type `int`.')
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError('Only valid indices for Point '
                             'are 0 and 1 (Got {})'.format(key))

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
