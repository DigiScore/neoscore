from neoscore.core import neoscore
from neoscore.core.music_font import MusicFont
from neoscore.core.point import ORIGIN
from neoscore.core.units import ZERO, Mm
from neoscore.western.metronome_mark import MetronomeMark
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestMetronomeMark(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff((Mm(0), Mm(0)), parent=None, length=Mm(100))

    def test_metronome_mark_layout(self):
        mark = MetronomeMark(ORIGIN, self.staff, "metNoteQuarterUp", "= 120")
        assert mark.music_text_obj.pos == ORIGIN
        assert mark.music_text_obj.parent == mark
        assert mark.plain_text_obj.x > ZERO  # Exact positions flake
        assert mark.plain_text_obj.y == ZERO
        assert mark.plain_text_obj.parent == mark

    def test_font_overrides(self):
        mfont = MusicFont("Bravura", Mm(5))
        tfont = neoscore.default_font.modified(size=Mm(20))
        mark = MetronomeMark(
            ORIGIN, self.staff, "metNoteQuarterUp", "= 120", mfont, tfont
        )
        assert mark.music_font == mfont
        assert mark.music_text_obj.music_font == mfont
        assert mark.plain_text_obj.font == tfont
