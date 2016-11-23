from brown.utils.point import Point


class AnchoredPoint(Point):
    """A Point with a parent anchor.

    This is identical to a Point except that it has an additional
    `parent` attribute. Its coordinates are then considered to be
    relative to the parent.

    Like a `Point`, the x and y values may be accessed by name,
    iteration, and indexing; however the `parent` attribute can
    only be accessed by name:

        >>> from brown.core.glyph import Glyph
        >>> some_grob = Glyph((10, 11), 'A')
        >>> p = AnchoredPoint(5, 6, some_grob)
        >>> p.x == p[0] == 5
        True
        >>> p.y == p[1] == 6
        True
        >>> x, y = p
        >>> x
        5
        >>> y
        6
        # The `parent` attribute must be referenced by index
        >>> p[2]
        Traceback (most recent call last):
        ...
        IndexError: Only valid indices for AnchoredPoint are 0 and 1 (got 2)
        >>> p.parent == some_grob
        True

    """
    def __init__(self, *args):
        """
        *args: One of:
            - An `x, y, parent` pair outside of a tuple
            - An `(x, y, parent)` 3-tuple
            - An existing AnchoredPoint
        """
        if len(args) == 3:
            self._x, self._y, self._parent = args
        elif len(args) == 1:
            if isinstance(args[0], tuple):
                self._x, self._y, self._parent = args[0]
            elif isinstance(args[0], type(self)):
                self._x = args[0].x
                self._y = args[0].y
                self._parent = args[0].parent
            else:
                raise ValueError('Invalid args for {}.__init__()'.format(
                    type(self).__name__))
        else:
            raise ValueError('Invalid args for {}.__init__()'.format(
                type(self).__name__))

        self._iter_index = 0


    ######## SPECIAL METHODS ########

    def __repr__(self):
        return '{}({}, {})'.format(type(self).__name__, self.x, self.y)

    ######## PRIVATE CLASS METHODS ########

    @classmethod
    def with_unit(cls, *args, unit=None):
        """Create a Point and ensure its coordinates are in a type of unit.

        *args: One of:
            - An `x, y, parent` pair outside of a tuple
            - An `(x, y, parent)` 3-tuple
            - An existing AnchoredPoint

        kwargs:
            unit (type): A Unit class.

        Example:
            >>> from brown.utils.units import Inch
            >>> from brown.core.glyph import Glyph
            >>> some_grob = Glyph((10, 11), 'A')
            >>> p = AnchoredPoint.with_unit(2, 3, unit=Inch)
            >>> print(p.x)
            2 inches
            >>> print(p.y)
            3 inches

        Warning: Due to the flexibility of constructor options in Points,
            `unit` must be passed as a keyword argument.

        TODO: Fix unnecessary explicit kwarg,
              rework constructor signature if needed.
        """
        if unit is None:
            raise TypeError('unit must be set to a Unit or subclass.'
                            ' (Did you forget to pass it as a kwarg?)')
        point = cls(*args)
        point.to_unit(unit)
        return point

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

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        self.setters_hook()

    def setters_hook(self):
        """Optional method to be called when an attribute changes.

        To set a change hook, instantiate a Point and set its `setters_hook`
        method to some arbitrary function. Any time an attribute is changed,
        this function will be called.

        Example:
            >>> class PointHolder:
            ...     def __init__(self):
            ...         self.point_setter_hook_called = False
            ...         self.point = AnchoredPoint(0, 0)
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
