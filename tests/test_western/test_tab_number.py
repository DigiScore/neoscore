from neoscore.core.music_char import MusicChar
from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm
from neoscore.western.tab_number import TabNumber
from neoscore.western.tab_staff import TabStaff

from ..helpers import AppTest


class TestTabClef(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = TabStaff(ORIGIN, None, Mm(200))

    def test_single_digit(self):
        tn = TabNumber(Mm(10), self.staff, 2, 1)
        assert tn.music_chars == [MusicChar(self.staff.music_font, "fingering1")]

    def test_multiple_digits(self):
        tn = TabNumber(Mm(10), self.staff, 2, 15)
        assert tn.music_chars == [
            MusicChar(self.staff.music_font, "fingering1"),
            MusicChar(self.staff.music_font, "fingering5"),
        ]

    def test_sanity_check_large_number_range(self):
        for n in range(0, 100):
            TabNumber(Mm(10), self.staff, 3, n)
