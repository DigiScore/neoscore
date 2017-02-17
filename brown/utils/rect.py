from brown.utils.point import Point


class Rect:

    """A rectangle data object."""

    def __init__(self, x, y, width, height):
        """
        Args:
            x (int, float, or Unit): The starting x position
            y (int, float, or Unit): The starting y position
            width (int, float, or Unit): The width of the rectangle
            height (int, float, or Unit): The height of the rectangle
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    ######## SPECIAL METHODS ########

    def __repr__(self):
        return '{}({}, {}, {}, {})'.format(
            type(self).__name__, self.x, self.y, self.width, self.height)

    ######## PUBLIC METHODS ########

    def to_unit(self, unit):
        """Translate properties to be of a certain unit type.

        Args:
            unit (type): A Unit class.

        Returns:
            Rect: the modified self rect.
        """
        self._x = unit(self.x)
        self._y = unit(self.y)
        self._width = unit(self.width)
        self._height = unit(self.height)
        return self

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point: The starting (usually top-left) corner of the rect"""
        # TODO: Implement this in reverse - x and y derived from pos,
        #       as in most similar cases in the codebase
        return Point(self.x, self.y)

    @property
    def x(self):
        """x (int, float, or Unit): The starting x position"""
        return self._x

    @property
    def y(self):
        """y (int, float, or Unit): The starting y position"""
        return self._y

    @property
    def width(self):
        """width (int, float, or Unit): The width of the rectangle"""
        return self._width

    @property
    def height(self):
        """height (int, float, or Unit): The height of the rectangle"""
        return self._height

    # TODO: work out setters
