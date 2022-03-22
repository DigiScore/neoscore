import unittest
from typing import Optional

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.music_char import MusicChar
from neoscore.models import notehead_tables
from neoscore.models.beat import Beat
from neoscore.utils.units import Mm
from neoscore.western.clef import Clef
from neoscore.western.notehead import Notehead
from neoscore.western.staff import Staff


class TestNotehead(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, length=Mm(10000))
        Clef(Mm(0), self.staff, "treble")

    def test_staff_position_middle_c_treble(self):
        assert Notehead(
            Mm(10), self.staff, "c'", Beat(1, 4)
        ).staff_pos == self.staff.unit(5)

    def test_staff_position_low_octaves(self):
        assert Notehead(
            Mm(10), self.staff, "c", Beat(1, 4)
        ).staff_pos == self.staff.unit(8.5)
        assert Notehead(
            Mm(10), self.staff, "c,", Beat(1, 4)
        ).staff_pos == self.staff.unit(12)
        assert Notehead(
            Mm(10), self.staff, "c,,", Beat(1, 4)
        ).staff_pos == self.staff.unit(15.5)
        assert Notehead(
            Mm(10), self.staff, "c,,,", Beat(1, 4)
        ).staff_pos == self.staff.unit(19)

    def test_staff_position_high_octaves(self):
        assert Notehead(
            Mm(10), self.staff, "c''", Beat(1, 4)
        ).staff_pos == self.staff.unit(1.5)
        assert Notehead(
            Mm(10), self.staff, "c'''", Beat(1, 4)
        ).staff_pos == self.staff.unit(-2)
        assert Notehead(
            Mm(10), self.staff, "c''''", Beat(1, 4)
        ).staff_pos == self.staff.unit(-5.5)
        assert Notehead(
            Mm(10), self.staff, "c'''''", Beat(1, 4)
        ).staff_pos == self.staff.unit(-9)

    def test_staff_position_with_accidentals(self):
        assert Notehead(
            Mm(10), self.staff, "cf'", Beat(1, 4)
        ).staff_pos == self.staff.unit(5)
        assert Notehead(
            Mm(10), self.staff, "cn'", Beat(1, 4)
        ).staff_pos == self.staff.unit(5)
        assert Notehead(
            Mm(10), self.staff, "cs'", Beat(1, 4)
        ).staff_pos == self.staff.unit(5)

    def test_staff_position_with_all_letter_names(self):
        assert Notehead(
            Mm(10), self.staff, "d'", Beat(1, 4)
        ).staff_pos == self.staff.unit(4.5)
        assert Notehead(
            Mm(10), self.staff, "e'", Beat(1, 4)
        ).staff_pos == self.staff.unit(4)
        assert Notehead(
            Mm(10), self.staff, "f'", Beat(1, 4)
        ).staff_pos == self.staff.unit(3.5)
        assert Notehead(
            Mm(10), self.staff, "g'", Beat(1, 4)
        ).staff_pos == self.staff.unit(3)
        assert Notehead(
            Mm(10), self.staff, "a'", Beat(1, 4)
        ).staff_pos == self.staff.unit(2.5)
        assert Notehead(
            Mm(10), self.staff, "b'", Beat(1, 4)
        ).staff_pos == self.staff.unit(2)

    def test_staff_position_on_later_flowable_line(self):
        assert Notehead(
            Mm(1000), self.staff, "c", Beat(1, 4)
        ).staff_pos == self.staff.unit(8.5)

    def assert_glyph_lookup(
        self,
        duration: Beat,
        glyph_name: str,
        table: Optional[notehead_tables.NoteheadTable] = None,
    ):
        if table:
            notehead = Notehead(
                Mm(10), self.staff, "c'", duration, notehead_table=table
            )
        else:
            notehead = Notehead(Mm(10), self.staff, "c'", duration)
        assert notehead.music_chars == [MusicChar(self.staff.music_font, glyph_name)]

    def test_glyph_lookup(self):
        self.assert_glyph_lookup(Beat(1, 4), "noteheadBlack")
        self.assert_glyph_lookup(Beat(3, 4), "noteheadHalf")
        self.assert_glyph_lookup(Beat(3, 2), "noteheadWhole")
        self.assert_glyph_lookup(Beat(3, 1), "noteheadDoubleWhole")

    def test_glyph_lookup_other_table(self):
        table = notehead_tables.STANDARD_WITH_PARENTHESES
        self.assert_glyph_lookup(Beat(1, 4), "noteheadBlackParens", table)
        self.assert_glyph_lookup(Beat(3, 4), "noteheadHalfParens", table)
        self.assert_glyph_lookup(Beat(3, 2), "noteheadWholeParens", table)
        self.assert_glyph_lookup(Beat(3, 1), "noteheadDoubleWholeParens", table)
