from PyQt5 import QtGui

from brown.config import config
from brown.utils import color


class PenInterface:
    """Interface for a generic drawing pen controlling path outline appearance.

    Currently only solid colors are supported.
    """

    def __init__(self, color, thickness=None):
        """
        Args:
            color (str or tuple): Either a hexadecimal color string or a
                3-tuple of RGB int's
        """
        # HACK: Initialize color to bright red to this not being set
        #       by color setter
        self._qt_object = QtGui.QPen(QtGui.QColor('#FF0000'))
        self.thickness = thickness
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
                raise TypeError(
                    'RGB tuple for BrushInterface must be len 3')
        elif isinstance(value, str):
            self._color = value
        else:
            raise TypeError
        self._qt_object.setColor(QtGui.QColor(self._color))

    @property
    def thickness(self):
        """Unit: The drawing thickness of the pen.

        If set to None, the value defaults to 0, a cosmetic pixel width.
        """
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if value is None:
            value = 0
        self._thickness = value
        self._qt_object.setWidthF(self._thickness)
