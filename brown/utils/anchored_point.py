from brown.utils.point import Point
from brown.utils.units import Unit


class AnchoredPoint(Point):
    """A Point with an optional parent anchor.

    This is identical to a Point except that it has an additional
    `parent` attribute. Its coordinates are then considered to be
    relative to the parent.
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

    ######## PUBLIC CLASS METHODS ########

    @classmethod
    def from_existing(cls, anchored_point):
        """Clone an AnchoredPoint.

        Args:
            anchored_point (AnchoredPoint): The anchored point to clone

        Returns: AnchoredPoint
        """
        return cls(anchored_point.x, anchored_point.y, anchored_point.parent)

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
