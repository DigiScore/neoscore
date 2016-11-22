from brown.core.glyph import Glyph
from brown.core.music_font import MusicFont


class MusicGlyph(Glyph):
    """
    A glyph with a MusicFont and convenient access to relevant SMuFL metadata.

    Unlike a Glyph, the text of a MusicGlyph may be passed either as a unicode
    character or as its corresponding canonical SMuFL name.
    """

    def __init__(self, pos, canonical_name, font=None, parent=None):
        # type check font is MusicFont before sending to init?
        code_point = font.glyph_info(canonical_name)['codepoint']
        super().__init__(pos, code_point, font, parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def font(self):
        """MusicFont: The glyph music font."""
        return self._font

    @font.setter
    def font(self, value):
        # TODO: Code below is redundant with super,
        #       find a way to use inheritance here
        if not isinstance(value, MusicFont):
            raise TypeError('MusicGlyph.font must be a MusicFont')
        self._font = value
        if self._interface:
            self._interface.font = value._interface
