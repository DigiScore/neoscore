from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import Mm
from neoscore.western import clef_type
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestClef(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(ORIGIN, None, Mm(200))

    def test_treble(self):
        clef = Clef(Mm(1), self.staff, clef_type.TREBLE)
        assert clef.clef_type == clef_type.TREBLE
        assert clef.pos == Point(Mm(1), self.staff.unit(3))
        assert clef.music_chars[0].canonical_name == "gClef"
        assert clef.middle_c_staff_position == self.staff.unit(5)
        assert clef.staff == self.staff

    def test_bass(self):
        clef = Clef(Mm(1), self.staff, clef_type.BASS)
        assert clef.clef_type == clef_type.BASS
        assert clef.pos == Point(Mm(1), self.staff.unit(1))
        assert clef.music_chars[0].canonical_name == "fClef"
        assert clef.middle_c_staff_position == self.staff.unit(-1)

    def test_init_with_str_clef_type(self):
        assert Clef(Mm(1), self.staff, "treble").clef_type == clef_type.TREBLE

    def test_breakable_length_with_no_other_clefs(self):
        clef = Clef(Mm(1), self.staff, clef_type.TREBLE)
        assert clef.breakable_length == Mm(200 - 1)

    def test_breakable_length_with_other_clefs(self):
        clef = Clef(Mm(1), self.staff, clef_type.TREBLE)
        later_clef = Clef(Mm(50), self.staff, clef_type.TREBLE)
        assert clef.breakable_length == Mm(50 - 1)

    def test_clef_type_setter_updates_other_attributes(self):
        clef = Clef(Mm(1), self.staff, clef_type.TREBLE)
        clef.clef_type = "bass"
        assert clef.clef_type == clef_type.BASS
        assert clef.pos == Point(Mm(1), self.staff.unit(1))
        assert clef.music_chars[0].canonical_name == "fClef"
        assert clef.middle_c_staff_position == self.staff.unit(-1)

    def test_supports_dynamic_position_clef_types(self):
        perc_staff_1 = Staff(ORIGIN, None, Mm(200), line_count=1)
        clef_1 = Clef(Mm(1), perc_staff_1, clef_type.PERCUSSION_1)
        assert clef_1.y == perc_staff_1.unit(0)
        assert clef_1.middle_c_staff_position == perc_staff_1.unit(0)

        perc_staff_2 = Staff(ORIGIN, None, Mm(200), line_count=3)
        clef_2 = Clef(Mm(1), perc_staff_2, clef_type.PERCUSSION_1)
        assert clef_2.y == perc_staff_2.unit(1)
        assert clef_2.middle_c_staff_position == perc_staff_2.unit(1)

        perc_staff_3 = Staff(ORIGIN, None, Mm(200), line_count=5)
        clef_3 = Clef(Mm(1), perc_staff_3, clef_type.PERCUSSION_1)
        assert clef_3.y == perc_staff_3.unit(2)
        assert clef_3.middle_c_staff_position == perc_staff_3.unit(2)
