from brown import config
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.core.pen_pattern import PenPattern
from brown.utils.units import GraphicUnit


class Pen:
    """Class for a generic drawing pen controlling fill patterns.

    Currently only solid colors are supported.
    """

    def __init__(self,
                 color='#000000',
                 thickness=None,
                 pattern=PenPattern.SOLID):
        """
        Args:
            color (Color or init tuple): The stroke color
            thickness (Unit): The stroke thickness.
                A value of `0` indicates Args cosmetic pixel width.
                Defaults to `config.DEFAULT_PEN_THICKNESS`.
            pattern (PenPattern or int): The stroke pattern.
                Defaults to a solid line.
        """
        if isinstance(color, Color):
            self._color = color
        elif isinstance(color, tuple):
            self._color = Color(*color)
        else:
            self._color = Color(color)
        self._thickness = (thickness if thickness is not None
                           else GraphicUnit(config.DEFAULT_PEN_THICKNESS))
        self._pattern = pattern
        self._interface = PenInterface(self,
                                       self.color,
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
        """Unit: The stroke thickness."""
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    @property
    def pattern(self):
        """PenPattern: The stroke pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
