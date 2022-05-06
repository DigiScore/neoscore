from neoscore.core.break_opportunity import BreakOpportunity
from neoscore.core.color import Color
from neoscore.core.flowable import Flowable
from neoscore.core.music_font import MusicFont
from neoscore.core.point import Point
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.western import barline_style
from neoscore.western.barline import Barline
from neoscore.western.barline_style import BarlineStyle
from neoscore.western.staff import Staff
from neoscore.western.tab_staff import TabStaff

from ..helpers import AppTest


class TestBarline(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff_1 = Staff((Mm(0), Mm(0)), self.flowable, Mm(100), line_spacing=Mm(2))
        self.staff_2 = Staff((Mm(0), Mm(30)), self.flowable, Mm(100))
        self.tab_staff = TabStaff((Mm(10), Mm(50)), self.flowable, Mm(100))

    def test_path_shape_with_same_staff_x_coords(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2])
        assert barline.paths[0].elements[0].pos == Point(Mm(0), Mm(0))
        assert barline.paths[0].elements[0].parent == barline.paths[0]
        assert barline.paths[0].elements[1].pos == Point(
            Unit(0), self.staff_2.height + self.staff_2.y
        )
        assert barline.paths[0].elements[1].parent == barline.paths[0]

    def test_path_shape_with_different_staff_x_coords(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.tab_staff])
        assert barline.paths[0].elements[0].pos == Point(Mm(0), Mm(0))
        assert barline.paths[0].elements[0].parent == barline.paths[0]
        assert barline.paths[0].elements[1].pos == Point(
            Unit(0), self.tab_staff.height + self.tab_staff.y
        )
        assert barline.paths[0].elements[1].parent == barline.paths[0]

    def test_multi_bar_barline_positions_on_same_staves(self):
        barline = Barline(
            Mm(15), [self.staff_1, self.staff_2], barline_style.THIN_DOUBLE
        )
        assert barline.paths[0].pos == Point(Unit(-0.454), Mm(0))
        assert barline.paths[1].pos == Point(Unit(-4.082), Mm(0))
        barline = Barline(Mm(15), [self.staff_1, self.staff_2], barline_style.END)
        assert barline.paths[0].pos == Point(Unit(-1.417), Mm(0))
        assert barline.paths[1].pos == Point(Unit(-6.973), Mm(0))

    def test_style_measurement_resolution_with_numeric_value(self):
        barline = Barline(Mm(15), [self.staff_1], [BarlineStyle(2)])
        assert barline.paths[0].pen.thickness == barline.unit(2)

    def test_style_measurement_resolution_with_unit_value(self):
        barline = Barline(Mm(15), [self.staff_1], [BarlineStyle(Mm(2))])
        assert barline.paths[0].pen.thickness == Mm(2)

    def test_style_measurement_resolution_with_engraving_default_key(self):
        barline = Barline(Mm(15), [self.staff_1], [BarlineStyle("hBarThickness")])
        assert barline.paths[0].pen.thickness == barline.unit(1.0)

    def test_style_measurement_resolution_with_missing_engraving_default_key(self):
        barline = Barline(Mm(15), [self.staff_1], [BarlineStyle("not a real key")])
        assert barline.paths[0].pen.thickness == barline.unit(0.16)

    def test_gap_applies_in_correct_order(self):
        barline = Barline(
            Mm(15), [self.staff_1], [BarlineStyle(gap_right=10), BarlineStyle()]
        )
        thickness = barline.unit(0.16)
        assert barline.paths[0].x == -thickness / 2
        assert barline.unit(barline.paths[1].x) == barline.unit(-10) - (thickness * 2)

    def test_font_override(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.tab_staff])
        assert barline.music_font == self.staff_1.music_font
        font = MusicFont("Bravura", Mm)
        barline = Barline(
            Mm(15), [self.staff_1, self.staff_2, self.tab_staff], font=font
        )
        assert barline.music_font == font

    def test_pen_colour(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2])
        assert barline.paths[0].pen.color == Color(0, 0, 0, 255)
        pen_color = Color(255, 0, 0)
        barline = Barline(
            Mm(15),
            [self.staff_1, self.staff_2],
            styles=(BarlineStyle(thickness="thinBarlineThickness", color=pen_color)),
        )
        assert barline.paths[0].pen.color == Color(255, 0, 0, 255)

    def test_break_hint_insertion(self):
        barline = Barline(
            Mm(15), [self.staff_1, self.staff_2], barline_style.THIN_DOUBLE
        )
        assert isinstance(barline._break_hint, BreakOpportunity)
        assert barline._break_hint.parent == barline
        assert barline._break_hint.pos == Point(ZERO, ZERO)

    def test_barline_separation(self):
        barline = Barline(
            Mm(15), [self.staff_1, self.staff_2, self.tab_staff], connected=False
        )
        assert len(barline.paths[0].elements) == 6
        assert barline.paths[0].elements[0].pos.y == Mm(0.0)
        assert barline.paths[0].elements[1].pos.y == Mm(8.0)
        assert barline.paths[0].elements[2].pos.y == Mm(30)
        assert barline.paths[0].elements[3].pos.y == Mm(37)
        assert barline.paths[0].elements[4].pos.y == Mm(50)
        assert barline.paths[0].elements[5].pos.y == Mm(62.5)
