from PyQt5 import QtGui


class BrushInterface:
    """Interface for a generic drawing brush controlling fill patterns.

    Currently only solid colors are supported.
    """

    def __init__(self, color):
        """
        Args:
            color (Color): The color of the brush.
        """
        # TEMP: Initialize color to bright red to signal this not being
        # overrided
        self._qt_object = QtGui.QBrush(QtGui.QColor('#ff0000'))
        self.color = color

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
