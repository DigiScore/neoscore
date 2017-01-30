from PyQt5 import QtWidgets

from brown.core import brown
from brown.interface.graphic_object_interface import GraphicObjectInterface


class TextObjectInterface(GraphicObjectInterface):

    _interface_class = QtWidgets.QGraphicsSimpleTextItem

    def __init__(self, pos, text, font):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            text (str): The text for the object
            font (FontInterface): The font object for the text
        """
        self._qt_object = self._interface_class('')
        self.text = text
        self.font = font
        self.pos = pos

    ######## PUBLIC PROPERTIES ########

    @property
    def text(self):
        """str: The text for the object"""
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._qt_object.setText(value)

    @property
    def font(self):
        """FontInterface: The font object for the text """
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self._qt_object.setFont(value._qt_object)

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self._qt_object)
