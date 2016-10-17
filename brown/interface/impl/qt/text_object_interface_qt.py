from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.core import brown
from brown.interface.abstract.text_object_interface import TextObjectInterface


class TextObjectInterfaceQt(TextObjectInterface):
    def __init__(self, x, y, text, font):
        self._x = x
        self._y = y
        self.text = text
        self.font = font
        self._qt_object = QtWidgets.QGraphicsSimpleTextItem(self.text)
        self._qt_object.setFont(self.font._qt_object)
        self._refresh_qt_object_position()

    def draw(self):
        brown._app_interface.scene.addItem(self._qt_object)

    def _refresh_qt_object_position(self):
        self._qt_object.setPos(self.x, self.y)

    def refresh_interface_properties(self):
        self._qt_object.setPos(self.x, self.y)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError
        else:
            self._text = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        # Refresh position with qt object
        self._refresh_qt_object_position()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        # Refresh position with qt object
        self._refresh_qt_object_position()
