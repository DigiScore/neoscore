from neoscore.core.brush import Brush
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm
from neoscore.western.brace import Brace
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestBrace(AppTest):
    def setUp(self):
        super().setUp()
        self.top_staff = Staff(ORIGIN, None, Mm(100))
        self.bottom_staff = Staff((Mm(0), Mm(20)), None, Mm(100))

    def test_scaling_alternate_glyphs(self):
        small_brace = Brace(Mm(0), [self.top_staff])
        assert small_brace.music_chars[0].canonical_name == "braceSmall"
        large_brace = Brace(Mm(0), [self.top_staff, self.bottom_staff])
        assert large_brace.music_chars[0].canonical_name == "braceLarge"

    def test_default_font_from_top_staff(self):
        large_staff = Staff(ORIGIN, None, Mm(100), line_spacing=Mm(3))
        small_staff = Staff((Mm(0), Mm(20)), None, Mm(100))
        brace = Brace(Mm(0), [large_staff, self.bottom_staff])
        assert brace.music_font == large_staff.music_font

    def test_font_override(self):
        large_staff = Staff(ORIGIN, None, Mm(100), line_spacing=Mm(3))
        font = MusicFont("Bravura", Mm)
        brace = Brace(Mm(0), [large_staff], font)
        assert brace.music_font == font

    def test_brush_override(self):
        brace = Brace(Mm(0), [self.top_staff], brush="#ff0000")
        assert brace.brush == Brush("#ff0000")

    def test_pen_override(self):
        brace = Brace(Mm(0), [self.top_staff], pen="#ff0000")
        assert brace.pen == Pen("#ff0000")
