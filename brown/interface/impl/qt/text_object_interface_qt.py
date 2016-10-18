from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.core import brown
from brown.interface.abstract.text_object_interface import TextObjectInterface


class TextObjectInterfaceQt(TextObjectInterface):
    def __init__(self, x, y, text, font):
        """
        Args:
            x (float): The x position relative to the document
            y (float): The y position relative to the document
            text (str): The text for the object
            font (FontInterface): The font object for the text
        """
        self.text = text
        self.font = font
        self._qt_object = QtWidgets.QGraphicsSimpleTextItem(self.text)
        self._qt_object.setFont(self.font._qt_object)
        self.x = x
        self.y = y

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        """float: The x position relative to the document."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._qt_object.setX(self._x)

    @property
    def y(self):
        """float: The y position relative to the document."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._qt_object.setY(self._y)

    @property
    def text(self):
        """str: The text for the object"""
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError
        else:
            self._text = value

    @property
    def font(self):
        """ font (FontInterface): The font object for the text """
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        # TODO: Propogate font change to qt object

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self._qt_object)
