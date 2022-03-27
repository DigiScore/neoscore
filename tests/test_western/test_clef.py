import unittest

from neoscore.core import neoscore
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import Mm
from neoscore.western import clef_type
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff


class TestClef(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
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
