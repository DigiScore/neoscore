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
        self.staff_1 = Staff((Mm(0), Mm(0)), self.flowable, Mm(100), Mm(2))
        self.staff_2 = Staff((Mm(0), Mm(30)), self.flowable, Mm(100))
        self.tab_staff_3 = TabStaff((Mm(10), Mm(50)), self.flowable, Mm(100))

    def test_path_shape_with_same_staff_x_coords(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2])
        assert barline.paths[0].elements[0].pos == Point(Mm(0), Mm(0))
        assert barline.paths[0].elements[0].parent == barline.paths[0]
        assert barline.paths[0].elements[1].pos == Point(
            Unit(0), self.staff_2.height + self.staff_2.y
        )
        assert barline.paths[0].elements[1].parent == barline.paths[0]

    def test_path_shape_with_different_staff_x_coords(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.tab_staff_3])
        assert barline.paths[0].elements[0].pos == Point(Mm(0), Mm(0))
        assert barline.paths[0].elements[0].parent == barline.paths[0]
        assert barline.paths[0].elements[1].pos == Point(
            Unit(0), self.tab_staff_3.height + self.tab_staff_3.y
        )
        assert barline.paths[0].elements[1].parent == barline.paths[0]

    def test_multi_bar_barline_positions_on_same_staffs(self):
        barline = Barline(
            Mm(15), [self.staff_1, self.staff_2], barline_style.THIN_DOUBLE
        )
        assert barline.paths[0].pos == Point(Unit(-0.454), Mm(0))
        assert barline.paths[1].pos == Point(Unit(-2.214), Mm(0))
        barline = Barline(Mm(15), [self.staff_1, self.staff_2], barline_style.END)
        assert barline.paths[0].pos == Point(Unit(-1.417), Mm(0))
        assert barline.paths[1].pos == Point(Unit(-5.106), Mm(0))

    def test_font_override(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.tab_staff_3])
        assert barline.music_font == self.staff_1.music_font
        font = MusicFont("Bravura", Mm)
        barline = Barline(
            Mm(15), [self.staff_1, self.staff_2, self.tab_staff_3], font=font
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
        assert barline._break_hint.parent == barline.paths[0]
        assert barline._break_hint.pos == Point(self.staff_1.unit(0.08), ZERO)

    def test_barline_separation(self):
        barline = Barline(
            Mm(15), [self.staff_1, self.staff_2, self.tab_staff_3], connected=False
        )
        assert len(barline.paths[0].elements) == 6
        assert barline.paths[0].elements[0].pos.y == Mm(0.0)
        assert barline.paths[0].elements[1].pos.y == Mm(8.0)
        assert barline.paths[0].elements[2].pos.y == Mm(30)
        assert barline.paths[0].elements[3].pos.y == Mm(37)
        assert barline.paths[0].elements[4].pos.y == Mm(50)
        assert barline.paths[0].elements[5].pos.y == Mm(62.5)
