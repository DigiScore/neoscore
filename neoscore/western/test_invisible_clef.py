import unittest

from neoscore.core import neoscore
from neoscore.utils.point import ORIGIN
from neoscore.utils.units import Mm
from neoscore.western.invisible_clef import InvisibleClef
from neoscore.western.staff import Staff


class TestInvisibleClef(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.staff = Staff(ORIGIN, None, Mm(200))

    def test_init_with_str_clef_type(self):
        assert InvisibleClef(Mm(1), self.staff, "treble").text == ""
        assert InvisibleClef(Mm(1), self.staff, "bass").text == ""
        assert InvisibleClef(Mm(1), self.staff, "bass_8vb").text == ""
        assert InvisibleClef(Mm(1), self.staff, "tenor").text == ""
        assert InvisibleClef(Mm(1), self.staff, "alto").text == ""
