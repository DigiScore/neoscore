from PyQt5 import QtGui

from brown.core.pen_pattern import PenPattern
from brown.interface.interface import Interface
from brown.utils.units import GraphicUnit


class PenInterface(Interface):
    """Interface for a generic drawing pen controlling path outline appearance.

    Currently only solid colors are supported.
    """

    def __init__(self, brown_object, color, thickness, pattern):
        """
        Args:
            color (Color): The color for the pen
            thickness (Unit): The stroke thickness of the pen
            pattern (PenPattern or int enum value): The stroke pattern.
                Defaults to a solid line.
        """
        super().__init__(brown_object)
        self.qt_object = QtGui.QPen()
        self.thickness = thickness
        self.color = color
        self.pattern = (pattern if isinstance(pattern, PenPattern)
                        else PenPattern(pattern))

    ######## PUBLIC PROPERTIES ########

    @property
    def color(self):
        """Color: The color for the pen.

        This setter propagates changes to the underlying Qt object.
        """
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.qt_object.setColor(QtGui.QColor(color.red,
                                             color.green,
                                             color.blue,
                                             color.alpha))

    @property
    def thickness(self):
        """Unit: The drawing thickness of the pen.

        If set to None, the value defaults to 0, a cosmetic pixel width.

        This setter propagates changes to the underlying Qt object.
        """
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value
        self.qt_object.setWidthF(GraphicUnit(value).value)

    @property
    def pattern(self):
        """PenPattern: The stroke pattern.

        This setter propagates changes to the underlying Qt object.
        """
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
        self.qt_object.setStyle(value.value)
