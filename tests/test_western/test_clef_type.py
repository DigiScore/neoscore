from neoscore.core.music_font import MusicFont
from neoscore.core.units import Mm
from neoscore.western.clef_type import CLEF_TYPE_SHORTHAND_NAMES, TREBLE, ClefType

from ..helpers import AppTest


class TestClef(AppTest):
    def test_all_pre_defined_types_have_valid_glyphs(self):
        font = MusicFont("Bravura", Mm)

        for clef_type in CLEF_TYPE_SHORTHAND_NAMES.values():
            font.glyph_info(clef_type.glyph_name, None)

    def test_from_def(self):
        assert ClefType.from_def(TREBLE) == TREBLE
        assert ClefType.from_def("treble") == TREBLE
        assert ClefType.from_def("TREBLE") == TREBLE
