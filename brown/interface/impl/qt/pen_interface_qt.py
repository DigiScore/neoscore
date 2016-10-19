from PyQt5 import QtGui

from brown.interface.abstract.pen_interface import PenInterface
from brown.utils import color



class PenInterfaceQt(PenInterface):
    """Interface for a generic drawing pen controlling path outline appearance.

    Currently only solid colors are supported.
    """

    def __init__(self, color):
        """
        Args:
            color (str or tuple): Either a hexadecimal color string or a
                3-tuple of RGB int's
        """
        self._qt_object = QtGui.QPen(QtGui.QColor('#DDDDDD'))
        self.color = color

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
                    'RGB tuple for BrushInterface[Qt] must be len 3')
        elif isinstance(value, str):
            self._color = value
        else:
            raise TypeError
        self._qt_object.setColor(self._color)
