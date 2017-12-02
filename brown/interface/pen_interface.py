from PyQt5 import QtGui

from brown.core.pen_pattern import PenPattern
from brown.interface.interface import Interface
from brown.utils.units import GraphicUnit


class PenInterface(Interface):
    """Interface for a pen controlling path outline appearance."""

    def __init__(self, brown_object, color, thickness, pattern,
                 join_style, cap_style):
        """
        Args:
            brown_object (Pen): The object this interface belongs to.
            color (Color):
            thickness (Unit):
            pattern (PenPattern):
            join_style (PenJoinStyle):
            cap_style (PenCapStyle):
        """
        super().__init__(brown_object)
        self.qt_object = QtGui.QPen()
        self.thickness = thickness
        self.color = color
        self.pattern = pattern
        self.join_style = join_style
        self.cap_style = cap_style

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
    def thickness(self, new_value):
        self._thickness = new_value
        self.qt_object.setWidthF(GraphicUnit(new_value).value)

    @property
    def pattern(self):
        """PenPattern: The stroke pattern.

        This setter propagates changes to the underlying Qt object.
        """
        return self._pattern

    @pattern.setter
    def pattern(self, new_value):
        self._pattern = new_value
        self.qt_object.setStyle(new_value.value)


    @property
    def join_style(self):
        """PenJoinStyle: The joint style.

        This setter propagates changes to the underlying Qt object.
        """
        return self._join_style

    @join_style.setter
    def join_style(self, new_value):
        self._join_style = new_value
        self.qt_object.setJoinStyle(new_value.value)

    @property
    def cap_style(self):
        """PenCapStyle: The cap style.

        This setter propagates changes to the underlying Qt object.
        """
        return self._cap_style

    @cap_style.setter
    def cap_style(self, new_value):
        self._cap_style = new_value
        self.qt_object.setCapStyle(new_value.value)
