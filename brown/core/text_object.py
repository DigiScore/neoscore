from brown.interface.text_object_interface import TextObjectInterface
from brown.core import brown
from brown.core.graphic_object import GraphicObject


class TextObject(GraphicObject):

    _interface_class = TextObjectInterface

    def __init__(self, x, y, text, font=None, parent=None):
        self._interface = None
        if font:
            self.font = font
        else:
            self.font = brown.text_font
        self.text = text
        self._interface = TextObject._interface_class(
            x,
            y,
            self.text,
            self.font._interface)
        super().__init__(x, y, parent=parent)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError
        else:
            self._text = value
            if self._interface:
                self._interface.text = value

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        if self._interface:
            self._interface.font = value._interface
