from brown.utils.point import Point
from brown.utils.units import Unit


class AnchoredPoint(Point):
    """A Point with an optional parent anchor.

    This is identical to a Point except that it has an additional
    `parent` attribute. Its coordinates are then considered to be
    relative to the parent.

    Like a `Point`, the x and y values may be accessed by name,
    iteration, and indexing; however the `parent` attribute can
    only be accessed by name:

        >>> from brown.core.text_object import TextObject
        >>> some_grob = TextObject((10, 11), 'A')
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
        IndexError: Only valid indices for AnchoredPoint are 0 and 1 (Got 2)
        >>> p.parent == some_grob
        True

    """
    def __init__(self, *args):
        """
        *args: One of:
            * An `x, y` pair outside of a tuple (parent will be None)
            * An `(x, y)` pair (parent will be None)
            * An `x, y, parent` triple outside of a tuple
            * An `(x, y, parent)` 3-tuple
            * An `(x, y)` pair and a `parent`
            * An `Point` and a `parent`
            * An existing `AnchoredPoint`
            * An existing `Point` (parent will be None)

        All of the following are valid init signatures:
            * `AnchoredPoint(5, 6)`
            * `AnchoredPoint((5, 6))`
            * `AnchoredPoint(5, 6, some_grob)`
            * `AnchoredPoint((5, 6, some_grob))`
            * `AnchoredPoint((5, 6), some_grob)`
            * `AnchoredPoint(some_existing_point, some_grob)`
            * `AnchoredPoint(some_existing_anchored_point)`
            * `AnchoredPoint(some_existing_point)`
        """
        if len(args) == 1:
            if isinstance(args[0], tuple):
                self._x = args[0][0]
                self._y = args[0][1]
                self._parent = args[0][2] if len(args[0]) == 3 else None
            elif isinstance(args[0], Point):
                self._x = args[0].x
                self._y = args[0].y
                self._parent = (args[0].parent
                                if isinstance(args[0], type(self)) else None)
            else:
                raise ValueError('Invalid args for {}.__init__()'.format(
                    type(self).__name__))
        elif len(args) == 2:
            if isinstance(args[0], (tuple, Point)):
                self._x, self._y = args[0]
                self._parent = args[1]
            else:
                self._x, self._y = args
                self._parent = None
        elif len(args) == 3:
            self._x, self._y, self._parent = args
        else:
            raise ValueError('Invalid args for {}.__init__()'.format(
                    type(self).__name__))

        self._iter_index = 0

    ######## SPECIAL METHODS ########

    def __eq__(self, other):
        """Two AnchoredPoints are equal if their attributes are all equal.

        Return: Bool
        """
        if isinstance(other, type(self)):
            return (self.x == other.x and
                    self.y == other.y and
                    self.parent == other.parent)
        else:
            return False

    def __add__(self, other):
        """`AnchoredPoint`s may be added with each other if they share a parent

        Returns: AnchoredPoint
        """
        if not isinstance(other, type(self)):
            raise TypeError('Cannot add "{}" and "{}"'.format(
                type(self).__name__, type(other).__name__))
        elif self.parent != other.parent:
            raise TypeError('Cannot add "{}"s with different parents'.format(
                type(self).__name__))
        return type(self)(self.x + other.x, self.y + other.y, self.parent)

    def __sub__(self, other):
        """`AnchoredPoint`s may be subtracted with each other if they share a parent

        Returns: AnchoredPoint
        """
        if not isinstance(other, type(self)):
            raise TypeError('Cannot subtract "{}" and "{}"'.format(
                type(self).__name__, type(other).__name__))
        elif self.parent != other.parent:
            raise TypeError('Cannot subtract "{}"s with different parents'.format(
                type(self).__name__))
        return type(self)(self.x - other.x, self.y - other.y, self.parent)

    def __mul__(self, other):
        """`AnchoredPoint`s may be multiplied with scalars.

        Returns: AnchoredPoint
        """
        if not isinstance(other, (Unit, int, float)):
            raise TypeError('Cannot multiply "{}" and "{}"'.format(
                type(self).__name__, type(other).__name__))
        return type(self)(self.x * other, self.y * other)

    def __repr__(self):
        return '{}({}, {}, parent={})'.format(type(self).__name__,
                                              self.x, self.y, self.parent)

    ######## PRIVATE CLASS METHODS ########

    @classmethod
    def with_unit(cls, *args, unit=None):
        """Create an AnchoredPoint and ensure its coordinates are in a type of unit.

        *args: One of:
            - An `x, y` pair outside of a tuple (parent will be None)
            - An `(x, y)` pair (parent will be None)
            - An `x, y, parent` triple outside of a tuple
            - An `(x, y, parent)` 3-tuple
            - An `(x, y)` pair and a `parent`
            - An existing AnchoredPoint
            - An existing Point (parent will be None)

        kwargs:
            unit (type): A Unit class.

        Example:
            >>> from brown.utils.units import Inch
            >>> from brown.core.text_object import TextObject
            >>> some_grob = TextObject((10, 11), 'A')
            >>> p = AnchoredPoint.with_unit(2, 3, unit=Inch)
            >>> print(p.x)
            Inch(2)
            >>> print(p.y)
            Inch(3)

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
    def parent(self):
        """GraphicObject or None: The parent of this point"""
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
