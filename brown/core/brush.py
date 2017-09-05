from brown.core.brush_pattern import BrushPattern
from brown.interface.brush_interface import BrushInterface
from brown.utils.color import Color


class Brush:

    """A specifier for fill patterns.

    In general, `Pen`s are responsible for drawing shape outlines
    while `Brush`es are responsible for filling in shapes.
    """

    def __init__(self, color='#000000', pattern=BrushPattern.SOLID):
        """
        Args:
            color (Color or args for Color): The brush color
            pattern (BrushPattern or int enum value): The brush fill pattern.
                Defaults to a solid color.
        """
        if isinstance(color, Color):
            self.color = color
        elif isinstance(color, tuple):
            self.color = Color(*color)
        else:
            self.color = Color(color)
        if isinstance(pattern, BrushPattern):
            self._pattern = pattern
        else:
            self._pattern = BrushPattern(pattern)
        self._interface = BrushInterface(self, self.color, self.pattern)

    ######## CONSTRUCOTRS ########

    @classmethod
    def from_existing(cls, brush):
        """Clone a brush.

        Args:
            brush (Brush): An existing brush.

        Returns: Brush
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
        """BrushPattern: The fill pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
