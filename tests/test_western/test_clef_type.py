import unittest

from neoscore.core import neoscore
from neoscore.core.music_font import MusicFont
from neoscore.utils.units import Mm
from neoscore.western.clef_type import CLEF_TYPE_SHORTHAND_NAMES, TREBLE, ClefType


class TestClef(unittest.TestCase):
    def test_all_pre_defined_types_have_valid_glyphs(self):
        neoscore.setup()
        font = MusicFont("Bravura", Mm)

        for clef_type in CLEF_TYPE_SHORTHAND_NAMES.values():
            font.glyph_info(clef_type.glyph_name, None)

    def test_from_def(self):
        assert ClefType.from_def(TREBLE) == TREBLE
        assert ClefType.from_def("treble") == TREBLE
        assert ClefType.from_def("TREBLE") == TREBLE
