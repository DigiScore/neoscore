from neoscore.core.point import ORIGIN, ZERO, Point
from neoscore.core.units import Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from neoscore.western.tremolo import Tremolo

from ..helpers import AppTest


class TestTremolo(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(ORIGIN, None, Mm(200))
        clef = Clef(ZERO, self.staff, "treble")
        self.cr1 = Chordrest(Mm(10), self.staff, ["c'"], (1, 2))
        self.cr2 = Chordrest(Mm(20), self.staff, ["d"], (1, 2))

    def test_init_with_int_indication_args(self):
        tremolo = Tremolo(ORIGIN, self.staff, 3)
        assert tremolo.parent == self.staff
        assert tremolo.glyph_name == "tremolo3"
        assert tremolo.pos.x == ZERO
        assert tremolo.pos.y == ZERO

    def test_init_with_smufl_indication_args(self):
        tremolo = Tremolo(ORIGIN, self.staff, "pendereckiTremolo")
        assert tremolo.parent == self.staff
        assert tremolo.glyph_name == "pendereckiTremolo"
        assert tremolo.pos.x == ZERO
        assert tremolo.pos.y == ZERO

    def test_ini_build_with_for_chordrest_function(self):
        tremolo = Tremolo.for_chordrest(self.cr2, 3)
        assert tremolo.parent == self.cr2
        assert tremolo.glyph_name == "tremolo3"
        assert tremolo.tremolo_position == Point(
            self.staff.unit(0.067), self.staff.unit(2.996)
        )
