from typing import Optional

from neoscore.core.flowable import Flowable
from neoscore.core.music_char import MusicChar
from neoscore.core.units import Mm
from neoscore.western import notehead_tables
from neoscore.western.clef import Clef
from neoscore.western.duration import Duration
from neoscore.western.notehead import Notehead
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestNotehead(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, length=Mm(10000))
        Clef(Mm(0), self.staff, "treble")

    def test_staff_position_middle_c_treble(self):
        assert Notehead(
            Mm(10), self.staff, "c'", Duration(1, 4)
        ).staff_pos == self.staff.unit(5)

    def test_staff_position_low_octaves(self):
        assert Notehead(
            Mm(10), self.staff, "c", Duration(1, 4)
        ).staff_pos == self.staff.unit(8.5)
        assert Notehead(
            Mm(10), self.staff, "c,", Duration(1, 4)
        ).staff_pos == self.staff.unit(12)
        assert Notehead(
            Mm(10), self.staff, "c,,", Duration(1, 4)
        ).staff_pos == self.staff.unit(15.5)
        assert Notehead(
            Mm(10), self.staff, "c,,,", Duration(1, 4)
        ).staff_pos == self.staff.unit(19)

    def test_staff_position_high_octaves(self):
        assert Notehead(
            Mm(10), self.staff, "c''", Duration(1, 4)
        ).staff_pos == self.staff.unit(1.5)
        assert Notehead(
            Mm(10), self.staff, "c'''", Duration(1, 4)
        ).staff_pos == self.staff.unit(-2)
        assert Notehead(
            Mm(10), self.staff, "c''''", Duration(1, 4)
        ).staff_pos == self.staff.unit(-5.5)
        assert Notehead(
            Mm(10), self.staff, "c'''''", Duration(1, 4)
        ).staff_pos == self.staff.unit(-9)

    def test_staff_position_with_accidentals(self):
        assert Notehead(
            Mm(10), self.staff, "cf'", Duration(1, 4)
        ).staff_pos == self.staff.unit(5)
        assert Notehead(
            Mm(10), self.staff, "cn'", Duration(1, 4)
        ).staff_pos == self.staff.unit(5)
        assert Notehead(
            Mm(10), self.staff, "cs'", Duration(1, 4)
        ).staff_pos == self.staff.unit(5)

    def test_staff_position_with_all_letter_names(self):
        assert Notehead(
            Mm(10), self.staff, "d'", Duration(1, 4)
        ).staff_pos == self.staff.unit(4.5)
        assert Notehead(
            Mm(10), self.staff, "e'", Duration(1, 4)
        ).staff_pos == self.staff.unit(4)
        assert Notehead(
            Mm(10), self.staff, "f'", Duration(1, 4)
        ).staff_pos == self.staff.unit(3.5)
        assert Notehead(
            Mm(10), self.staff, "g'", Duration(1, 4)
        ).staff_pos == self.staff.unit(3)
        assert Notehead(
            Mm(10), self.staff, "a'", Duration(1, 4)
        ).staff_pos == self.staff.unit(2.5)
        assert Notehead(
            Mm(10), self.staff, "b'", Duration(1, 4)
        ).staff_pos == self.staff.unit(2)

    def test_staff_position_on_later_flowable_line(self):
        assert Notehead(
            Mm(1000), self.staff, "c", Duration(1, 4)
        ).staff_pos == self.staff.unit(8.5)

    def assert_glyph_lookup(
        self,
        duration: Duration,
        glyph_name: str,
        table: Optional[notehead_tables.NoteheadTable] = None,
    ):
        if table:
            notehead = Notehead(Mm(10), self.staff, "c'", duration, table=table)
        else:
            notehead = Notehead(Mm(10), self.staff, "c'", duration)
        assert notehead.music_chars == [MusicChar(self.staff.music_font, glyph_name)]

    def test_glyph_lookup(self):
        self.assert_glyph_lookup(Duration(1, 4), "noteheadBlack")
        self.assert_glyph_lookup(Duration(3, 4), "noteheadHalf")
        self.assert_glyph_lookup(Duration(3, 2), "noteheadWhole")
        self.assert_glyph_lookup(Duration(3, 1), "noteheadDoubleWhole")

    def test_glyph_lookup_other_table(self):
        table = notehead_tables.STANDARD_WITH_PARENTHESES
        self.assert_glyph_lookup(Duration(1, 4), "noteheadBlackParens", table)
        self.assert_glyph_lookup(Duration(3, 4), "noteheadHalfParens", table)
        self.assert_glyph_lookup(Duration(3, 2), "noteheadWholeParens", table)
        self.assert_glyph_lookup(Duration(3, 1), "noteheadDoubleWholeParens", table)

    def test_pitch_setter_from_def(self):
        note = Notehead(Mm(10), self.staff, "c'", Duration(1, 4))
        note.pitch = "c"
        assert note.pitch.letter == "c"

    def test_glyph_override(self):
        note = Notehead(
            Mm(10),
            self.staff,
            "d",
            Duration(1, 4),
            glyph_override="noteheadBlackParens",
        )
        assert note.music_chars == [
            MusicChar(self.staff.music_font, "noteheadBlackParens")
        ]
