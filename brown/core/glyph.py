from brown.core.text_object import TextObject


class InvalidGlyphLengthError(Exception):
    pass


class Glyph(TextObject):
    """
    Same as a TextObject with the limitation that its text
    can have at most one character
    """

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError
        if len(value) != 1:
            raise InvalidGlyphLengthError('Glyph text must be of length 1')
        else:
            self._text = value
