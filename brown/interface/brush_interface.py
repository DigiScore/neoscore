from PyQt5 import QtGui


class BrushInterface:
    """Interface for a generic drawing brush controlling fill patterns.

    Currently only solid colors are supported.
    """

    def __init__(self, color, pattern):
        """
        Args:
            color (Color): The color of the brush.
            pattern (FillPattern): The fill pattern of the brush.
        """
        # Initialize color to bright red to signal this not being
        # set correctly by color setter
        self._qt_object = QtGui.QBrush(QtGui.QColor('#ff0000'))
        self.color = color
        self.pattern = pattern

    ######## PUBLIC PROPERTIES ########

    @property
    def color(self):
        """Color: The color for the brush"""
        return self._colorterm

    @color.setter
    def color(self, color):
        self._color = color
        self._qt_object.setColor(QtGui.QColor(color.red,
                                              color.green,
                                              color.blue,
                                              color.alpha))

    @property
    def pattern(self):
        """FillPattern: The fill pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
        self._qt_object.setStyle(self.pattern.value)
