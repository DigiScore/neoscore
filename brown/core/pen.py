from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.config import config
from brown.utils.units import GraphicUnit


class Pen:
    """Class for a generic drawing pen controlling fill patterns.

    Currently only solid colors are supported.
    """

    _interface_class = PenInterface

    def __init__(self, color='#000000', thickness=None):
        """
        Args:
            color (Color or args for Color): The stroke color
            thickness (Unit): The stroke thickness
        """
        if isinstance(color, Color):
            self.color = color
        elif isinstance(color, tuple):
            self.color = Color(*color)
        else:
            self.color = Color(color)
        self.thickness = thickness
        self._create_interface()

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
        if value is None:
            value = GraphicUnit(config.DEFAULT_PEN_THICKNESS)
        self._thickness = value

    ######## PRIVATE METHODS ########

    def _create_interface(self):
        """Construct an interface and store it in self._interface.

        This should be called by self.__init__().
        """
        self._interface = self._interface_class(self.color, self.thickness)
