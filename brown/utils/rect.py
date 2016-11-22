from brown.utils.point import Point


class Rect:

    """A rectangle data object."""

    def __init__(self, x, y, width, height):
        """
        Args:
            x (int, float, or BaseUnit): The starting x position
            y (int, float, or BaseUnit): The starting y position
            width (int, float, or BaseUnit): The width of the rectangle
            height (int, float, or BaseUnit): The height of the rectangle
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    ######## CLASS METHODS ########

    @classmethod
    def with_unit(cls, x, y, width, height, unit):
        """Initialize a Rect and convert its values to a unit.

        Args:
            x (int, float, or BaseUnit): The starting x position
            y (int, float, or BaseUnit): The starting y position
            width (int, float, or BaseUnit): The width of the rectangle
            height (int, float, or BaseUnit): The height of the rectangle
            unit (type): A BaseUnit class

        Returns: Rect
        """
        return cls(unit(x), unit(y),
                   unit(width), unit(height))


    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        """x (int, float, or BaseUnit): The starting x position"""
        return self._x

    @property
    def y(self):
        """y (int, float, or BaseUnit): The starting y position"""
        return self._y

    @property
    def width(self):
        """width (int, float, or BaseUnit): The width of the rectangle"""
        return self._width

    @property
    def height(self):
        """height (int, float, or BaseUnit): The height of the rectangle"""
        return self._height

    # TODO: work out setters
