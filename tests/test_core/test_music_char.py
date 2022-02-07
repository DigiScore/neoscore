import unittest

from brown.core import brown
from brown.core.music_char import MusicChar
from brown.core.music_font import MusicFont
from brown.utils.units import Unit


class TestMusicChar(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.font = MusicFont("Bravura", Unit)

    def test_glyph_info_calculation(self):
        self.assertEqual(
            MusicChar(self.font, "brace").glyph_info, self.font.glyph_info("brace")
        )

    def test_glyph_info_calculation_with_alternate(self):
        self.assertEqual(
            MusicChar(self.font, "brace", 1).glyph_info,
            self.font.glyph_info("brace", 1),
        )
