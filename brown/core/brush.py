from brown.core.fill_pattern import FillPattern
from brown.interface.brush_interface import BrushInterface
from brown.utils.color import Color


class Brush:
    """Class for a generic drawing brush controlling fill patterns.

    Currently only solid colors are supported.
    """

    _interface_class = BrushInterface

    def __init__(self, color='#000000', pattern=FillPattern.SOLID):
        """
        Args:
            color (Color or args for Color): The brush color
            pattern (FillPattern or int enum value): The brush fill pattern.
                Defaults to a solid color.
        """
        if isinstance(color, Color):
            self.color = color
        elif isinstance(color, tuple):
            self.color = Color(*color)
        else:
            self.color = Color(color)
        if isinstance(pattern, FillPattern):
            self.pattern = pattern
        else:
            self.pattern = FillPattern(pattern)
        self._create_interface()

    ######## CONSTRUCOTRS ########

    @classmethod
    def from_existing(cls, brush):
        """Clone a brush.

        Args:
            brush (Brush): An existing brush.
        """
        return cls(brush.color, brush.pattern)

    ######## PUBLIC PROPERTIES ########

    @property
    def color(self):
        """Color: The color for the brush"""
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def pattern(self):
        """FillPattern: The fill pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value


    ######## PRIVATE METHODS ########

    def _create_interface(self):
        """Construct an interface and store it in self._interface.

        This should be called by self.__init__().
        """
        self._interface = self._interface_class(self.color, self.pattern)
