from neoscore.core.brush import Brush
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.utils.point import ORIGIN
from neoscore.utils.units import ZERO, Inch, Mm
from neoscore.western.tab_clef import TabClef
from neoscore.western.tab_staff import TabStaff

from ..helpers import AppTest


class TestTabClef(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = TabStaff(ORIGIN, None, Mm(200))

    def test_default_glyph(self):
        clef = TabClef(ZERO, self.staff)
        assert clef.music_chars == [MusicChar(self.staff.music_font, "6stringTabClef")]

    def test_allows_glyph_override(self):
        clef = TabClef(ZERO, self.staff, "4stringTabClef")
        assert clef.music_chars == [MusicChar(self.staff.music_font, "4stringTabClef")]

    def test_font_defaults_to_staff_font(self):
        clef = TabClef(ZERO, self.staff)
        assert clef.music_font == self.staff.music_font

    def test_font_override(self):
        other_font = MusicFont("Bravura", Inch)
        clef = TabClef(ZERO, self.staff)
        assert clef.music_font == self.staff.music_font

    def test_brush_default(self):
        clef = TabClef(Mm(10), self.staff)
        assert clef.brush == Brush()

    def test_brush_override(self):
        clef = TabClef(Mm(10), self.staff, brush="#ff0000")
        assert clef.brush == Brush("#ff0000")

    def test_pen_default_is_no_pen(self):
        clef = TabClef(Mm(10), self.staff)
        assert clef.pen == Pen.no_pen()

    def test_pen_override(self):
        clef = TabClef(Mm(10), self.staff, pen="#ff0000")
        assert clef.pen == Pen("#ff0000")

    def test_breakable_length_goes_to_staff_end(self):
        clef = TabClef(ZERO, self.staff)
        assert clef.breakable_length == Mm(200)
        clef = TabClef(Mm(50), self.staff)
        assert clef.breakable_length == Mm(150)
