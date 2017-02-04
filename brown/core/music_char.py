class MusicChar:
    """A SMuFL music character.


    Attributes:
        font (MusicFont): The font used to derivce SMuFL spec information
            about this glyph.
        canonical_name (str): The canonical SMuFL name of this font
        alternate_number (int or None): An optional alternate glyph code.
    """

    def __init__(self, font, glyph_name, alternate_number=None):
        """
        Args:
            font (MusicFont): The music font to be used. If not specified,
                the font is taken from the ancestor staff.
            glyph_name (str): The canonical SMuFL name of the glyph
            alternate_number (int or None): An optional alternate glyph code.

        Note:
            If an alternate number is given, `self.canonical_name` will be
            different than the `glyph_name` passed here.

            For instance, to access the alternate glyph 'braceSmall', you
            must go through the parent non-optional glyph 'brace'.
            Since 'braceSmall' is the first listed alternate glyph given
            for 'brace', we access it with `alternate_number = 1`:

                `MusicChar(some_font, 'brace', 1)`
        """
        self.font = font
        self._glyph_info = self.font.glyph_info(glyph_name, alternate_number)

    ######## PUBLIC PROPERTIES ########

    @property
    def canonical_name(self):
        return self.glyph_info['canonicalName']

    @property
    def codepoint(self):
        return self.glyph_info['codepoint']

    @property
    def glyph_info(self):
        """dict: The aggregated SMuFL metadata for this glyph"""
        return self._glyph_info
