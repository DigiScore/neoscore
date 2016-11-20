from brown.utils.point import Point


class Rect:

    """A rectangle data object."""

    def __init__(self, *args):
        """
        Args:
            Either:
                start (Point or tuple): The top left corner of the rectangle
                end (Point or tuple): The bottom right corner of the rectangle
            Or:
                x (int, float, or BaseUnit): The starting x position
                y (int, float, or BaseUnit): The starting y position
                width (int, float, or BaseUnit): The width of the rectangle
                height (int, float, or BaseUnit): The height of the rectangle
        """
        if len(args) == 2:
            self._x, self._y = args[0]
            self._width = args[1][0] - self._x
            self._height = args[1][1] - self._y
        elif len(args) == 4:
            self._x = args[0]
            self._y = args[1]
            self._width = args[2]
            self._height = args[3]
        else:
            raise TypeError('Invalid init signature for Rect')

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
