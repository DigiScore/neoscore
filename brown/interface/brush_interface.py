from PyQt5 import QtGui

from brown.interface.interface import Interface


class BrushInterface(Interface):
    """Interface for a generic drawing brush controlling fill patterns.

    Currently only solid colors are supported.
    """

    def __init__(self, brown_object, color, pattern):
        """
        Args:
            brown_object (Brush): The object this interface belongs to
            color (Color): The color of the brush.
            pattern (BrushPattern): The fill pattern of the brush.
        """
        # Initialize color to bright red to signal this not being
        # set correctly by color setter
        super().__init__(brown_object)
        self.qt_object = QtGui.QBrush(QtGui.QColor('#ff0000'))
        self.color = color
        self.pattern = pattern

    ######## PUBLIC PROPERTIES ########

    @property
    def color(self):
        """Color: The color for the brush.

        This setter automatically propagates changes to the
        underlying Qt object.
        """
        return self._colorterm

    @color.setter
    def color(self, color):
        self._color = color
        self.qt_object.setColor(QtGui.QColor(color.red,
                                             color.green,
                                             color.blue,
                                             color.alpha))

    @property
    def pattern(self):
        """BrushPattern: The fill pattern.

        This setter automatically propagates changes to the
        underlying Qt object.
        """
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
        self.qt_object.setStyle(self.pattern.value)
