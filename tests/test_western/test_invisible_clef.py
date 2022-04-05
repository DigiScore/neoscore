from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm
from neoscore.western.invisible_clef import InvisibleClef
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestInvisibleClef(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(ORIGIN, None, Mm(200))

    def test_init_with_str_clef_type(self):
        assert InvisibleClef(Mm(1), self.staff, "treble").text == ""
        assert InvisibleClef(Mm(1), self.staff, "bass").text == ""
        assert InvisibleClef(Mm(1), self.staff, "bass_8vb").text == ""
        assert InvisibleClef(Mm(1), self.staff, "tenor").text == ""
        assert InvisibleClef(Mm(1), self.staff, "alto").text == ""
