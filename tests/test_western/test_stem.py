from neoscore.core.directions import DirectionY
from neoscore.core.flowable import Flowable
from neoscore.core.path_element import LineTo, MoveTo
from neoscore.core.point import Point
from neoscore.core.units import Mm
from neoscore.western.staff import Staff
from neoscore.western.stem import Stem

from ..helpers import AppTest, assert_path_els_equal


class TestStem(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))

    def test_stem_direction(self):
        stem = Stem((Mm(0), Mm(0)), self.staff, DirectionY.UP, Mm(10))
        assert stem.direction == DirectionY.UP
        assert stem.direction.value == -1

        stem = Stem((Mm(0), Mm(0)), self.staff, DirectionY.DOWN, Mm(10))
        assert stem.direction == DirectionY.DOWN
        assert stem.direction.value == 1

    def test_default_pen_uses_engraving_default_thickness(self):
        stem = Stem((Mm(0), Mm(0)), self.staff, DirectionY.UP, Mm(10))
        assert (
            stem.pen.thickness
            == self.staff.music_font.engraving_defaults["stemThickness"]
        )

    def test_stem_line_respects_stem_direction(self):
        # stem direction UP
        stem = Stem((Mm(0), Mm(0)), self.staff, DirectionY.UP, Mm(10))
        assert stem.pos == Point(Mm(0), Mm(0))
        assert len(stem.elements) == 2

        # path origin moves to x, y == 0,0
        assert_path_els_equal(stem.elements[0], MoveTo(Point(Mm(0), Mm(0)), stem))

        # path draw line -10 (up direction)
        assert_path_els_equal(stem.elements[1], LineTo(Point(Mm(0), Mm(-10)), stem))

        # stem direction DOWN
        stem = Stem((Mm(10), Mm(10)), self.staff, DirectionY.DOWN, Mm(10))
        assert stem.pos == Point(Mm(10), Mm(10))
        assert len(stem.elements) == 2

        # path origin moves to x, y == 0,0
        assert_path_els_equal(stem.elements[0], MoveTo(Point(Mm(0), Mm(0)), stem))

        # path draw line +10 (down direction)
        assert_path_els_equal(stem.elements[1], LineTo(Point(Mm(0), Mm(10)), stem))
