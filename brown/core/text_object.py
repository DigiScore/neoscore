from brown.interface.impl.qt import text_object_interface_qt
from brown.utils import color
from brown.core import brown


class TextObject:

    _interface_class = text_object_interface_qt.TextObjectInterfaceQt

    def __init__(self, x, y, text, font=None):
        self._x = x
        self._y = y
        self.text = text
        if font:
            self.font = font
        else:
            self.font = brown.text_font
        self._interface = TextObject._interface_class(
            self.x, self.y, self.text, self.font._interface)

    def render(self):
        self._interface.render()

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
        self.gl_x = value
        self._interface.x = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._interface.y = self._y

    @property
    def pen(self):
        """
        Pen: The pen to draw outlines with
        """
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value
        if self._pen:
            self._interface.pen = self._pen._interface

    @property
    def brush(self):
        """
        Brush: The brush to draw outlines with
        """
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value
        if self._brush:
            self._interface.brush = self._brush._interface
