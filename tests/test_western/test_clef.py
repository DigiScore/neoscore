import unittest

from neoscore.core import neoscore
from neoscore.models.clef_type import ClefType
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import Mm
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff


class TestClef(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.staff = Staff(ORIGIN, None, Mm(200))

    def test_treble(self):
        clef = Clef(Mm(1), self.staff, ClefType.TREBLE)
        assert clef.clef_type == ClefType.TREBLE
        assert clef.pos == Point(Mm(1), self.staff.unit(3))
        assert clef.music_chars[0].canonical_name == "gClef"
        assert clef.middle_c_staff_position == self.staff.unit(5)
        assert clef.staff == self.staff

    def test_bass(self):
        clef = Clef(Mm(1), self.staff, ClefType.BASS)
        assert clef.clef_type == ClefType.BASS
        assert clef.pos == Point(Mm(1), self.staff.unit(1))
        assert clef.music_chars[0].canonical_name == "fClef"
        assert clef.middle_c_staff_position == self.staff.unit(-1)

    def test_bass_8vb(self):
        clef = Clef(Mm(1), self.staff, ClefType.BASS_8VB)
        assert clef.clef_type == ClefType.BASS_8VB
        assert clef.pos == Point(Mm(1), self.staff.unit(1))
        assert clef.music_chars[0].canonical_name == "fClef8vb"
        assert clef.middle_c_staff_position == self.staff.unit(-6.5)

    def test_tenor(self):
        clef = Clef(Mm(1), self.staff, ClefType.TENOR)
        assert clef.clef_type == ClefType.TENOR
        assert clef.pos == Point(Mm(1), self.staff.unit(1))
        assert clef.music_chars[0].canonical_name == "cClef"
        assert clef.middle_c_staff_position == self.staff.unit(1)

    def test_alto(self):
        clef = Clef(Mm(1), self.staff, ClefType.ALTO)
        assert clef.clef_type == ClefType.ALTO
        assert clef.pos == Point(Mm(1), self.staff.unit(2))
        assert clef.music_chars[0].canonical_name == "cClef"
        assert clef.middle_c_staff_position == self.staff.unit(2)

    def test_init_with_str_clef_type(self):
        assert Clef(Mm(1), self.staff, "treble").clef_type == ClefType.TREBLE
        assert Clef(Mm(1), self.staff, "bass").clef_type == ClefType.BASS
        assert Clef(Mm(1), self.staff, "bass_8vb").clef_type == ClefType.BASS_8VB
        assert Clef(Mm(1), self.staff, "tenor").clef_type == ClefType.TENOR
        assert Clef(Mm(1), self.staff, "alto").clef_type == ClefType.ALTO

    def test_length_with_no_other_clefs(self):
        clef = Clef(Mm(1), self.staff, ClefType.TREBLE)
        assert clef.breakable_length == Mm(200 - 1)

    def test_length_with_other_clefs(self):
        clef = Clef(Mm(1), self.staff, ClefType.TREBLE)
        later_clef = Clef(Mm(50), self.staff, ClefType.TREBLE)
        assert clef.breakable_length == Mm(50 - 1)
