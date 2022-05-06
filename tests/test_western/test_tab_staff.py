from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN
from neoscore.core.units import ZERO, Mm
from neoscore.western.tab_staff import TabStaff

from ..helpers import AppTest, assert_almost_equal


class TestTabStaff(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = TabStaff(ORIGIN, None, Mm(200))

    def test_default_pen_thickness_matches_smufl(self):
        staff = TabStaff(ORIGIN, None, Mm(100))
        assert (
            staff.pen.thickness
            == staff.music_font.engraving_defaults["staffLineThickness"]
        )

    def test_allows_pen_override(self):
        pen = Pen("#ff0000")
        staff = TabStaff(ORIGIN, None, Mm(100), pen=pen)
        assert staff.pen == pen

    def test_line_spacing_default(self):
        staff = TabStaff(ORIGIN, None, Mm(100))
        assert staff.line_spacing == Mm(2.5)

    def test_line_spacing_override(self):
        staff = TabStaff(ORIGIN, None, Mm(100), line_spacing=Mm(2))
        assert staff.line_spacing == Mm(2)

    def test_line_count_default(self):
        staff = TabStaff(ORIGIN, None, Mm(100))
        assert staff.line_count == 6

    def test_line_count_default(self):
        staff = TabStaff(ORIGIN, None, Mm(100), line_count=10)
        assert staff.line_count == 10

    def test_music_font_size_derived_from_line_spacing(self):
        staff = TabStaff(ORIGIN, None, Mm(100), line_spacing=Mm(2))
        assert staff.music_font.family_name == "Bravura"
        self.assertAlmostEqual(staff.music_font.unit.CONVERSION_RATE, 3.7795296)

    def test_music_font_override(self):
        font = MusicFont("Bravura", Mm)
        staff = TabStaff(ORIGIN, None, Mm(100), music_font=font)
        assert staff.music_font == font

    def test_string_y(self):
        staff = TabStaff(ORIGIN, None, Mm(100))
        assert staff.string_y(1) == ZERO
        assert_almost_equal(staff.string_y(2), staff.unit(1.5))
        assert_almost_equal(staff.string_y(3), staff.unit(3))
        assert_almost_equal(staff.string_y(4), staff.unit(4.5))
        assert_almost_equal(staff.string_y(5), staff.unit(6))
        assert_almost_equal(staff.string_y(6), staff.unit(7.5))
