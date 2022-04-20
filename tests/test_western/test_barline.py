from neoscore.core.flowable import Flowable
from neoscore.core.music_font import MusicFont
from neoscore.core.point import Point
from neoscore.core.units import Mm
from neoscore.western import barline_style
from neoscore.western.barline import Barline
from neoscore.western.staff import Staff

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
        assert barline.paths[0].elements[0].pos == Point(Mm(0), Mm(0))
        assert barline.paths[0].elements[0].parent == barline.paths[0]
        assert barline.paths[0].elements[1].pos == Point(Unit(0), self.staff_1.barline_extent[0])
        # assert barline.paths.elements[1].parent == self.staff_2

    def test_path_shape_with_different_staff_x_coords(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.staff_3])
        assert barline.line_path.elements[0].pos == Point(Mm(0), Mm(0))
        assert barline.line_path.elements[0].parent == barline.line_path
        assert barline.line_path.elements[1].pos == Point(Mm(5), self.staff_3.height)
        assert barline.line_path.elements[1].parent == self.staff_3

    def test_font_override(self):
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.staff_3])
        assert barline.music_font == self.staff_1.music_font
        font = MusicFont("Bravura", Mm)
        barline = Barline(Mm(15), [self.staff_1, self.staff_2, self.staff_3], font)
        assert barline.music_font == font

    # def test_barline_style_info(self):
    #     bar_style_single = barline_style.SINGLE
    #     # bar_style_thick_double = barline_style.THICK_DOUBLE
    #     bar_style_end = barline_style.END
    #
    #     assert bar_style_single.style[0] == "thinBarlineThickness"
    #     # assert bar_style_thick_double.lines[1] == "thickBarlineThickness"
    #     assert bar_style_end.lines[0] == "thinBarlineThickness"
    #     assert bar_style_end.lines[1] == "thickBarlineThickness"
