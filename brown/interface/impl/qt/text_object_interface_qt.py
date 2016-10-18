from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.core import brown
from brown.interface.abstract.text_object_interface import TextObjectInterface


class TextObjectInterfaceQt(TextObjectInterface):
    def __init__(self, x, y, text, font):
        self.text = text
        self.font = font
        self._qt_object = QtWidgets.QGraphicsSimpleTextItem(self.text)
        self._qt_object.setFont(self.font._qt_object)
        self.x = x
        self.y = y


    def render(self):
        brown._app_interface.scene.addItem(self._qt_object)

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
        self._qt_object.setX(self._x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._qt_object.setY(self._y)
