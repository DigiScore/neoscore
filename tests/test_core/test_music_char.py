import unittest

from neoscore.core import neoscore
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.utils.units import Unit


class TestMusicChar(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
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
