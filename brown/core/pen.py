from brown import config
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.core.pen_pattern import PenPattern
from brown.utils.units import GraphicUnit


class Pen:
    """Class for a generic drawing pen controlling fill patterns.

    Currently only solid colors are supported.
    """

    _interface_class = PenInterface

    def __init__(self,
                 color='#000000',
                 thickness=None,
                 pattern=PenPattern.SOLID):
        """
        Args:
            color (Color or args for Color): The stroke color
            thickness (Unit): The stroke thickness
            pattern (PenPattern): The stroke pattern.
                Defaults to a solid line.
        """
        if isinstance(color, Color):
            self.color = color
        elif isinstance(color, tuple):
            self.color = Color(*color)
        else:
            self.color = Color(color)
        self.thickness = thickness
        self.pattern = pattern
        self._interface = self._interface_class(self.color,
                                                self.thickness,
                                                self.pattern)

    ######## CONSTRUCOTRS ########

    @classmethod
    def from_existing(cls, pen):
        """Clone a pen.

        Args:
            pen (Pen): An existing pen.
        """
        return cls(pen.color, pen.thickness, pen.pattern)

    ######## PUBLIC PROPERTIES ########

    @property
    def color(self):
        """Color: The color for the pen"""
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def thickness(self):
        """Unit: The stroke thickness.

        A value of 0 (in any unit) indicates a cosmetic pixel width.
        Setting to None will default to config.DEFAULT_PEN_THICKNESS
        """
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = (value if value is not None
                           else GraphicUnit(config.DEFAULT_PEN_THICKNESS))

    @property
    def pattern(self):
        """PenPattern: The stroke pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
