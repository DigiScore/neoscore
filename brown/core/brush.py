from brown.interface.brush_interface import BrushInterface
from brown.utils.color import Color


class Brush:
    """Class for a generic drawing brush controlling fill patterns.

    Currently only solid colors are supported.
    """

    _interface_class = BrushInterface

    def __init__(self, color='#000000'):
        """
        Args:
            color (Color or args for Color): The brush color
        """
        if isinstance(color, Color):
            self.color = color
        elif isinstance(color, tuple):
            self.color = Color(*color)
        else:
            self.color = Color(color)
        self._create_interface()

    ######## PUBLIC PROPERTIES ########

    @property
    def color(self):
        """Color: The color for the brush"""
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    ######## PRIVATE METHODS ########

    def _create_interface(self):
        """Construct an interface and store it in self._interface.

        This should be called by self.__init__().
        """
        self._interface = self._interface_class(self.color)
