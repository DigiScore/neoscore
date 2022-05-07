from neoscore.core.music_font import MusicFont
from neoscore.core.path_element import LineTo, MoveTo
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import ZERO, Mm
from neoscore.western.staff import Staff
from neoscore.western.system_line import SystemLine

from ..helpers import AppTest, assert_path_els_equal


class TestSystemLine(AppTest):
    def setUp(self):
        super().setUp()
        self.top_staff = Staff(ORIGIN, None, Mm(100))
        self.bottom_staff = Staff((Mm(0), Mm(20)), None, Mm(100))
        self.staves = [self.top_staff, self.bottom_staff]

    def test_font_override(self):
        line = SystemLine(self.staves)
        assert line.music_font == self.top_staff.music_font
        explicit_font = MusicFont("Bravura", Mm(10))
        line = SystemLine(self.staves, font=explicit_font)
        assert line.music_font == explicit_font

    def test_pen_override(self):
        line = SystemLine(self.staves)
        assert (
            line.pen.thickness
            == self.top_staff.music_font.engraving_defaults["staffLineThickness"]
        )
        line = SystemLine(self.staves, pen=Pen("#ff0000"))
        assert line.pen == Pen("#ff0000")

    def test_path_drawing(self):
        line = SystemLine(self.staves)
        assert_path_els_equal(
            line.elements, [MoveTo(ORIGIN, line), LineTo(Point(ZERO, Mm(27)), line)]
        )
