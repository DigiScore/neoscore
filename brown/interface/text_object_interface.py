from PyQt5 import QtWidgets
from PyQt5 import QtGui

from brown.core import brown
from brown.interface.graphic_object_interface import GraphicObjectInterface


class TextObjectInterface(GraphicObjectInterface):
    def __init__(self, x, y, text, font, parent=None):
        """
        Args:
            x (float): The x position relative to the document
            y (float): The y position relative to the document
            text (str): The text for the object
            font (FontInterface): The font object for the text
            parent: The parent interface object
        """
        self.text = text
        self.font = font
        self._qt_object = QtWidgets.QGraphicsSimpleTextItem(self.text)
        self._qt_object.setFont(self.font._qt_object)
        self.x = x
        self.y = y
        self.parent = parent

    ######## PUBLIC PROPERTIES ########

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
