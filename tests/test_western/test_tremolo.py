from neoscore.core.point import ORIGIN
from neoscore.core.units import ZERO, Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from neoscore.western.tremolo import Tremolo

from ..helpers import AppTest, assert_almost_equal


class TestTremolo(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(ORIGIN, None, Mm(200))
        clef = Clef(ZERO, self.staff, "treble")
        self.cr1 = Chordrest(Mm(10), self.staff, ["c'"], (1, 2))
        self.cr2 = Chordrest(Mm(20), self.staff, ["d"], (1, 2))
        self.cr3 = Chordrest(Mm(30), self.staff, [], (1, 2))
        self.cr4 = Chordrest(Mm(40), self.staff, ["b,"], (1, 1))
        self.cr5 = Chordrest(Mm(50), self.staff, ["c"], (1, 8))
        self.cr6 = Chordrest(Mm(60), self.staff, ["f'"], (1, 8))
        self.cr7 = Chordrest(Mm(70), self.staff, ["c", "e", "g"], (1, 8))
        self.cr8 = Chordrest(Mm(80), self.staff, ["f'", "a'", "c''"], (1, 8))

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

    def test_init_build_with_for_chordrest_function(self):
        tremolo = Tremolo.for_chordrest(self.cr2, 3)
        assert tremolo.parent == self.cr2
        assert tremolo.glyph_name == "tremolo3"
        assert tremolo.pos == tremolo.tremolo_position
        assert_almost_equal(tremolo.pos.x, self.staff.unit(0.067), 2)
        assert_almost_equal(tremolo.pos.y, self.staff.unit(2.996), 2)

    def test_position_of_tremolo_attachment_point(self):
        cr = Chordrest.tremolo_attachment_point(self.cr2)
        assert_almost_equal(cr.x, self.staff.unit(0.067), 2)
        assert_almost_equal(cr.y, self.staff.unit(2.996), 2)

    def test_init_build_with_for_chordrest_function_rest(self):
        tremolo = Tremolo.for_chordrest(self.cr3, 3)
        assert tremolo.parent == self.cr3
        assert tremolo.glyph_name == "tremolo3"
        assert tremolo.pos == tremolo.tremolo_position
        assert_almost_equal(tremolo.pos.x, self.staff.unit(0.567), 2)
        assert_almost_equal(tremolo.pos.y, self.staff.unit(0.427), 2)

    def test_init_build_with_for_chordrest_function_wholenote(self):
        tremolo = Tremolo.for_chordrest(self.cr4, 5)
        assert tremolo.parent == self.cr4
        assert tremolo.glyph_name == "tremolo5"
        assert tremolo.pos == tremolo.tremolo_position
        assert_almost_equal(tremolo.pos.x, self.staff.unit(1.701), 2)
        assert_almost_equal(tremolo.pos.y, self.staff.unit(3.996), 2)

    def test_init_build_with_for_chordrest_function_8th_notes_up_stem(self):
        tremolo_up = Tremolo.for_chordrest(self.cr5, 2)
        assert tremolo_up.parent == self.cr5
        assert tremolo_up.glyph_name == "tremolo2"
        assert tremolo_up.pos == tremolo_up.tremolo_position
        assert_almost_equal(tremolo_up.pos.x, self.staff.unit(0.067), 2)
        assert_almost_equal(tremolo_up.pos.y, self.staff.unit(3.496), 2)

    def test_init_build_with_for_chordrest_function_8th_notes_down_stem(self):
        tremolo_down = Tremolo.for_chordrest(self.cr6, 2)
        assert tremolo_down.parent == self.cr6
        assert tremolo_down.glyph_name == "tremolo2"
        assert tremolo_down.pos == tremolo_down.tremolo_position
        assert_almost_equal(tremolo_down.pos.x, self.staff.unit(-0.06), 2)
        assert_almost_equal(tremolo_down.pos.y, self.staff.unit(2.004), 2)

    def test_init_build_with_for_mulitnote_chordrest_function_8th_notes_up_stem(self):
        tremolo_up = Tremolo.for_chordrest(self.cr7, 2)
        assert tremolo_up.parent == self.cr7
        assert tremolo_up.glyph_name == "tremolo2"
        assert tremolo_up.pos == tremolo_up.tremolo_position
        assert_almost_equal(tremolo_up.pos.x, self.staff.unit(0.067), 2)
        assert_almost_equal(tremolo_up.pos.y, self.staff.unit(1.496), 2)

    def test_init_build_with_for_mulitnote_chordrest_function_8th_notes_down_stem(self):
        tremolo_down = Tremolo.for_chordrest(self.cr8, 2)
        assert tremolo_down.parent == self.cr8
        assert tremolo_down.glyph_name == "tremolo2"
        assert tremolo_down.pos == tremolo_down.tremolo_position
        assert_almost_equal(tremolo_down.pos.x, self.staff.unit(-0.06), 2)
        assert_almost_equal(tremolo_down.pos.y, self.staff.unit(2.004), 2)
