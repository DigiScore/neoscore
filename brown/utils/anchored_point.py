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

        >>> from brown.core import brown
        >>> from brown.core.text_object import TextObject
        >>> brown.setup()
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
    def __init__(self, x, y, parent=None):
        """
        Args:
            x (float or Unit):
            y (float or Unit):
            parent (GraphicObject or None): The object this point
                is anchored to. If None, this object acts like a Point
        """
        super().__init__(x, y)
        self._parent = parent

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
        return type(self)(self.x * other, self.y * other, self.parent)

    def __repr__(self):
        return '{}({}, {}, parent={})'.format(type(self).__name__,
                                              self.x, self.y, self.parent)

    ######## PRIVATE CLASS METHODS ########

    @classmethod
    def with_unit(cls, x, y, parent, unit):
        """Create an AnchoredPoint and ensure its coordinates are in a type of unit.

        Args:
            x (float or Unit):
            y (float or Unit):
            parent (GraphicObject): The object this point is anchored to.
            unit (type): A Unit class.

        Returns: AnchoredPoint

        TODO: Replace this method with the pattern:

                  Point(x, y).to_unit()

              and make to_unit() return the point (instead of None)
        """
        point = cls(x, y, parent)
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
