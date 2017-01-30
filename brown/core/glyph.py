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

    @property
    def _origin_offset(self):
        """The origin offset override for this glyph."""
        return None

    ######## PUBLIC METHODS ########

    def position_y_baseline(self, y):
        """Position the glyph such that its baseline is on `y`"""
        self.y = y - self.font.ascent

    def _render_complete(self, pos):
        """Render the entire object.

        Args:
            pos (Point): The rendering position in document space for drawing.

        Returns: None
        """
        self._interface = self._interface_class(
            pos,
            self.text,
            self.font._interface,
            origin_offset=self._origin_offset,
        )
        self._interface.render()
