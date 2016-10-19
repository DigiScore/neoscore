from brown.interface.impl.qt import text_object_interface_qt
from brown.config.config import DEFAULT_FONT
from brown.utils import color


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
        self._x = value
        self._interface.x = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._interface.y = self._y

    @property
    def default_color(self):
        """str: A hexadecimal color string value.

        If this is set to an RGB tuple it will be converted to and stored
        in hexadecimal form
        """
        return self._color

    @default_color.setter
    def default_color(self, value):
        if isinstance(value, tuple):
            if len(value) == 3:
                self._default_color = color.rgb_to_hex(value)
            else:
                raise ValueError(
                    'RGB tuple for PenInterface[Qt] must be len 3')
        elif isinstance(value, str):
            self._default_color = value
        else:
            raise TypeError
        self._interface.default_color = self._default_color
