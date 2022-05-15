from neoscore.core.glyph_info import GlyphInfo
from neoscore.core.music_font import MusicFont
from neoscore.core.raw_music_char import RawMusicChar
from neoscore.core.units import Unit

from ..helpers import AppTest


class TestRawMusicChar(AppTest):
    def setUp(self):
        super().setUp()
        self.font = MusicFont("Bravura", Unit)

    def test_glyph_info(self):
        char = RawMusicChar(self.font, " ")
        assert char.codepoint == " "
        assert char.bounding_rect is None
        assert char.glyph_info == GlyphInfo("[RAW CHAR]", " ", "", None, None, None)
