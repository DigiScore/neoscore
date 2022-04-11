from neoscore.core.flowable import Flowable
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.core.point import Point
from neoscore.core.units import Mm
from neoscore.western.barline import Barline
from neoscore.western.staff import Staff
from neoscore.western.barline_style import BarLineStyle

from ..helpers import AppTest


class TestBarline(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff_1 = Staff((Mm(0), Mm(0)), self.flowable, Mm(100), Mm(2))
        self.staff_2 = Staff((Mm(0), Mm(30)), self.flowable, Mm(100))
        self.staff_3 = Staff((Mm(10), Mm(50)), self.flowable, Mm(100))

    def test_path_shape_with_same_staff_x_coords(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2])
        assert barline.elements[0].pos == Point(Mm(0), Mm(0))
        assert barline.elements[0].parent == barline
        assert barline.elements[1].pos == Point(Mm(15), self.staff_2.height)
        assert barline.elements[1].parent == self.staff_2

    def test_path_shape_with_different_staff_x_coords(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.staff_3])
        assert barline.elements[0].pos == Point(Mm(0), Mm(0))
        assert barline.elements[0].parent == barline
        assert barline.elements[1].pos == Point(Mm(5), self.staff_3.height)
        assert barline.elements[1].parent == self.staff_3

    def test_font_override(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.staff_3])
        assert barline.music_font == self.staff_1.music_font
        font = MusicFont("Bravura", Mm)
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.staff_3], font)
        assert barline.music_font == font

    def test_default_pen_uses_engraving_default_thickness(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2])
        assert (
            barline.pen.thickness
            == self.staff_1.music_font.engraving_defaults["thinBarlineThickness"]
        )

    def test_pen_override(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2], pen="#ff0000")
        assert barline.pen == Pen("#ff0000")

    def test_bar_line_style_enum(self):
        barline = Barline(Mm(15),
                          [self.staff_1, self.staff_2],
                          style=BarLineStyle.SINGLE)
        assert barline.style["pattern"] == 1
