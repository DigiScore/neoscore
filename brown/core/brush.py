from brown.core.brush_pattern import BrushPattern
from brown.interface.brush_interface import BrushInterface
from brown.utils.color import Color


class Brush:

    """A specifier for fill patterns.

    In general, `Pen`s are responsible for drawing shape outlines
    while `Brush`es are responsible for filling in shapes.
    """

    def __init__(self, color="#000000", pattern=BrushPattern.SOLID):
        """
        Args:
            color (Color or args for Color): The brush color
            pattern (BrushPattern): The brush fill pattern.
                Defaults to a solid color.
        """
        if isinstance(color, Color):
            self._color = color
        elif isinstance(color, tuple):
            self._color = Color(*color)
        else:
            self._color = Color(color)
        self._pattern = pattern
        self._regenerate_interface()

    @classmethod
    def from_existing(cls, brush):
        """Clone a brush.

        Args:
            brush (Brush): An existing brush.

        Returns: Brush
        """
        return cls(brush.color, brush.pattern)

    def _regenerate_interface(self):
        self._interface = BrushInterface(self.color, self.pattern)

    @property
    def color(self) -> Color:
        """The color for the brush"""
        return self._color

    @color.setter
    def color(self, value: Color):
        self._color = value
        self._regenerate_interface()

    @property
    def pattern(self) -> BrushPattern:
        """The fill pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, value: BrushPattern):
        self._pattern = value
        self._regenerate_interface()

    @property
    def interface(self) -> BrushInterface:
        return self._interface


NO_BRUSH = Brush(pattern=BrushPattern.NO_BRUSH)
