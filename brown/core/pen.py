from brown.interface.pen_interface import PenInterface
from brown.utils import color


class Pen:
    """Class for a generic drawing pen controlling fill patterns.

    Currently only solid colors are supported.
    """

    _interface_class = PenInterface

    def __init__(self, color='#000000', thickness=None):
        """
        Args:
            color (str or tuple): Either a hexadecimal color string or a
                3-tuple of RGB int's
            thickness (Unit): The stroke thickness
        """
        self.color = color
        self.thickness = thickness
        self._create_interface()

    ######## PUBLIC PROPERTIES ########

    @property
    def color(self):
        """str: A hexadecimal color string value.

        If this is set to an RGB tuple it will be converted to and stored
        in hexadecimal form
        """
        return self._color

    @color.setter
    def color(self, value):
        if isinstance(value, tuple):
            if len(value) == 3:
                self._color = color.rgb_to_hex(value)
            else:
                raise ValueError(
                    'RGB tuple for PenInterface must be len 3')
        elif isinstance(value, str):
            self._color = value
        else:
            raise TypeError

    @property
    def thickness(self):
        """Unit: The stroke thickness"""
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    ######## PRIVATE METHODS ########

    def _create_interface(self):
        """Construct an interface and store it in self._interface.

        This should be called by self.__init__().
        """
        self._interface = self._interface_class(self.color, self.thickness)
