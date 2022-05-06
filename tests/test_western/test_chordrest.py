from neoscore.core.directions import DirectionY
from neoscore.core.flowable import Flowable
from neoscore.core.music_char import MusicChar
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import Mm
from neoscore.western import notehead_tables
from neoscore.western.accidental_type import AccidentalType
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.duration import Duration
from neoscore.western.key_signature import KeySignature
from neoscore.western.pitch import Pitch
from neoscore.western.staff import Staff
from tests.helpers import assert_almost_equal, render_scene

from ..helpers import AppTest


class TestChordrest(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable(Point(Mm(0), Mm(0)), None, Mm(10000), Mm(100))
        self.staff = Staff(ORIGIN, self.flowable, Mm(100))
        self.font = self.staff.music_font
        Clef(Mm(0), self.staff, "treble")

    def test_rest_y_defaults_to_staff_center(self):
        # 5 line staff
        chord = Chordrest(Mm(1), self.staff, None, (1, 4))
        assert chord.rest.y == self.staff.unit(2)
        # 1 line staff
        other_staff = Staff(ORIGIN, self.flowable, Mm(100), line_count=1)
        chord = Chordrest(Mm(1), other_staff, None, (1, 4))
        assert chord.rest.y == other_staff.unit(0)

    def test_rest_y_override(self):
        chord = Chordrest(Mm(1), self.staff, None, (1, 4), self.staff.unit(-1))
        assert chord.rest.y == self.staff.unit(-1)

    def test_notehead_glyph_overrides(self):
        pitches = [
            ("c", AccidentalType.SHARP, 3),
            ("c'", notehead_tables.DIAMOND.short),
        ]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.noteheads[0].music_chars == [MusicChar(self.font, "noteheadBlack")]
        assert chord.noteheads[1].music_chars == [
            MusicChar(self.font, "noteheadDiamondBlack")
        ]

    def test_notes_setter_triggers_rebuild(self):
        chord = Chordrest(Mm(1), self.staff, [], Duration(1, 4))
        assert chord.notes == []
        assert len(chord.noteheads) == 0
        assert chord.rest is not None
        chord.notes = ["c"]
        assert chord.notes == ["c"]
        assert len(chord.noteheads) == 1
        assert chord.rest is None

    def test_table_setter_triggers_rebuild(self):
        chord = Chordrest(Mm(1), self.staff, ["c"], Duration(1, 4))
        assert chord.noteheads[0].music_chars == [MusicChar(self.font, "noteheadBlack")]
        chord.table = notehead_tables.DIAMOND
        assert chord.noteheads[0].music_chars == [
            MusicChar(self.font, "noteheadDiamondBlack")
        ]

    def test_notes_none_converted_to_empty_list(self):
        chord = Chordrest(Mm(1), self.staff, None, Duration(1, 4))
        assert chord.notes == []

    def test_duration_setter_triggers_rebuild(self):
        chord = Chordrest(Mm(1), self.staff, ["c"], Duration(1, 4))
        assert chord.noteheads[0].music_chars == [MusicChar(self.font, "noteheadBlack")]
        chord.duration = (1, 1)
        assert chord.noteheads[0].music_chars == [MusicChar(self.font, "noteheadWhole")]

    def test_rest_y_setter_triggers_rebuild(self):
        chord = Chordrest(Mm(1), self.staff, None, (1, 4))
        assert chord.rest.y == self.staff.unit(2)
        chord.rest_y = self.staff.unit(-1)
        assert chord.rest.y == self.staff.unit(-1)

    def test_invisible_notehead(self):
        chord = Chordrest(
            Mm(1),
            self.staff,
            ["c"],
            Duration(1, 4),
            table=notehead_tables.INVISIBLE,
        )
        assert chord.noteheads[0].music_chars == []

    def test_ledger_line_positions(self):
        pitches = ["c", "b", "f''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.ledger_line_positions == [
            self.staff.unit(5),
            self.staff.unit(-3),
            self.staff.unit(-2),
            self.staff.unit(-1),
        ]

    def test_ledger_line_positions_with_different_clef(self):
        Clef(Mm(10), self.staff, "bass")
        pitches = ["e,,", "d,", "e"]
        chord = Chordrest(Mm(15), self.staff, pitches, Duration(1, 4))
        assert chord.ledger_line_positions == [
            self.staff.unit(5),
            self.staff.unit(-2),
            self.staff.unit(-1),
        ]

    # todo - fix error here
    def test_rhythm_dot_positions_with_rest(self):
        chord = Chordrest(Mm(1), self.staff, None, Duration(7, 16))
        dots = list(chord.rhythm_dot_positions)
        dots.sort(key=lambda d: d.x)
        assert_almost_equal(
            dots[0], Point(self.staff.unit(1.52), self.staff.unit(1.5)), epsilon=2
        )
        assert_almost_equal(
            dots[1], Point(self.staff.unit(2.02), self.staff.unit(1.5)), epsilon=2
        )

    def test_rhythm_dot_positions_with_noteheads(self):
        pitches = ["e,,", "d,", "e''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(7, 16))
        dots = list(chord.rhythm_dot_positions)
        dots.sort(key=lambda d: d.x)
        dots.sort(key=lambda d: d.y)
        assert_almost_equal(
            dots[0], Point(self.staff.unit(0.743), self.staff.unit(-3.5)), epsilon=2
        )
        assert_almost_equal(
            dots[1], Point(self.staff.unit(1.243), self.staff.unit(-3.5)), epsilon=2
        )
        assert_almost_equal(
            dots[2], Point(self.staff.unit(0.743), self.staff.unit(7.5)), epsilon=2
        )
        assert_almost_equal(
            dots[3], Point(self.staff.unit(1.243), self.staff.unit(7.5)), epsilon=2
        )
        assert_almost_equal(
            dots[4], Point(self.staff.unit(0.743), self.staff.unit(10.5)), epsilon=2
        )
        assert_almost_equal(
            dots[5], Point(self.staff.unit(1.243), self.staff.unit(10.5)), epsilon=2
        )

    def test_furthest_notehead_with_one_note(self):
        pitches = ["b"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.furthest_notehead.pitch == Pitch.from_str("b")
        pitches = ["f''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.furthest_notehead.pitch == Pitch.from_str("f''")
        pitches = ["c,,,,,"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.furthest_notehead.pitch == Pitch.from_str("c,,,,,")

    def test_furthest_notehead_with_many_notes(self):
        pitches = ["b'", "bs"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.furthest_notehead.pitch == Pitch.from_str("b'")
        pitches = ["b", "b,,,,"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.furthest_notehead.pitch == Pitch.from_str("b,,,,")
        pitches = ["f'''", "b,"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.furthest_notehead.pitch == Pitch.from_str("f'''")
        pitches = ["c", "c,,,,,", "b", "c''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.furthest_notehead.pitch == Pitch.from_str("c,,,,,")

    def test_highest_notehead(self):
        pitches = ["c", "b", "c''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.highest_notehead.pitch == Pitch.from_str("c''")

    def test_lowest_notehead(self):
        pitches = ["c", "b", "c''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.lowest_notehead.pitch == Pitch.from_str("c")

    def test_highest_and_lowest_notehead_same_with_one_note(self):
        pitches = ["c"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.highest_notehead == chord.lowest_notehead

    def test_extra_attachment_point_with_rest(self):
        chord = Chordrest(Mm(1), self.staff, None, Duration(1, 4))
        assert_almost_equal(
            chord.extra_attachment_point,
            Point(self.staff.unit(0.504), self.staff.unit(-0.613)),
            2,
        )

    def test_extra_attachment_point_with_upward_stem(self):
        chord = Chordrest(Mm(1), self.staff, ["c"], Duration(1, 4))
        assert_almost_equal(
            chord.extra_attachment_point,
            Point(self.staff.unit(-0.515), self.staff.unit(6.605)),
            2,
        )

    def test_extra_attachment_point_with_upward_stem(self):
        chord = Chordrest(Mm(1), self.staff, ["f'"], Duration(1, 4))
        assert_almost_equal(
            chord.extra_attachment_point,
            Point(self.staff.unit(0.545), self.staff.unit(-1.605)),
            2,
        )

    def test_stem_direction_down(self):
        pitches = ["c", "b", "c'''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.stem_direction == DirectionY.DOWN

    def test_stem_direction_up(self):
        pitches = ["c,,,,,,", "b", "c''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.stem_direction == DirectionY.UP

    def test_stem_direction_down_with_one_note_at_staff_center(self):
        pitches = ["b"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.stem_direction == DirectionY.DOWN

    def test_stem_direction_at_center_with_one_line_staff(self):
        staff = Staff(Point(Mm(0), Mm(0)), None, Mm(100), line_count=1)
        Clef(Mm(0), staff, "percussion_2")
        pitches = ["c"]
        chord = Chordrest(Mm(1), staff, pitches, Duration(1, 4))
        assert chord.stem_direction == DirectionY.UP

    def test_stem_direction_override(self):
        pitches = ["b"]
        chord = Chordrest(
            Mm(1),
            self.staff,
            pitches,
            Duration(1, 4),
            stem_direction=DirectionY.UP,
        )
        assert chord.stem_direction == DirectionY.UP
        # Setting stem_direction = None should revert to default 1
        chord.stem_direction = None
        assert chord.stem_direction == DirectionY.DOWN

    def test_stem_height_min(self):
        pitches = ["b"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert_almost_equal(chord.stem_height, self.staff.unit(3))

    def test_stem_height_fitted(self):
        pitches = ["c''", "g,"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert_almost_equal(chord.stem_height, self.staff.unit(10.5))

    def test_stem_vertical_attachment_pos(self):
        pitches = ["c''", "g,"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.stem.y == self.staff.unit(6.332)
        chord.stem_direction = DirectionY.DOWN
        assert chord.stem.y == self.staff.unit(-1.832)

    def test_position_noteheads_around_stem(self):
        pitches = ["c", "d", "e", "f", "c''", "e''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Duration(1, 4))
        assert chord.noteheads[0].x == self.staff.unit(-1.12)
        assert chord.noteheads[1].x == self.staff.unit(-0.06)
        assert chord.noteheads[2].x == self.staff.unit(-1.12)

    def test_end_to_end(self):
        staff = Staff((Mm(0), Mm(0)), None, Mm(100), line_spacing=Mm(1))
        unit = staff.unit
        clef = Clef(unit(0), staff, "treble")
        KeySignature(clef.bounding_rect.width + unit(0.5), staff, "g_major")
        # Chord with ledgers, dots, flags, and accidentals
        Chordrest(unit(8), staff, ["gs''", "cf", "a,,,,"], Duration(3, 64))
        # Rest with dots
        Chordrest(unit(20), staff, None, Duration(7, 128))
        render_scene()
