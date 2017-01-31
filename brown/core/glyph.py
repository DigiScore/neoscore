from brown.core.text_object import TextObject


class InvalidGlyphLengthError(Exception):
    pass


class Glyph(TextObject):
    """A TextObject with exactly one character."""

    ######## PUBLIC PROPERTIES ########

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError
        elif len(value) != 1:
            raise InvalidGlyphLengthError('Glyph text must be of length 1')
        else:
            self._text = value

    @property
    def baseline_y(self):
        """GraphicUnit: The y coordinate of the glyph's baseline"""
        return self.y + self.font.ascent

    ######## PRIVATE PROPERTIES ########

    @property
    def _bounding_rect(self):
        """The bounding rect override for this glyph."""
        return None

    ######## PUBLIC METHODS ########

    def position_y_baseline(self, y):
        """Position the glyph such that its baseline is on `y`"""
        self.y = y - self.font.ascent
