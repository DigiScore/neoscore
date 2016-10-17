from brown.interface.impl.qt import text_object_interface_qt
from brown.config.config import DEFAULT_FONT


class TextObject:

    _interface_class = text_object_interface_qt.TextObjectInterfaceQt

    def __init__(self, x, y, text, font=None):
        self._x = x
        self._y = y
        self.text = text
        if font:
            self.font = font
        else:
            self.font = DEFAULT_FONT
        self._interface = TextObject._interface_class(
            self.x, self.y, self.text, self.font._interface)

    def draw(self):
        self._interface.draw()

    def _refresh_interface_object_position(self):
        self._interface.x = self.x
        self._interface.y = self.y
        self._interface.refresh_interface_properties()

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
        self._refresh_interface_object_position()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        # Refresh position with qt object
        self._refresh_interface_object_position()
