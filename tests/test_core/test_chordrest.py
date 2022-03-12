import unittest

from neoscore.core import neoscore
from neoscore.core.chordrest import Chordrest
from neoscore.core.clef import Clef
from neoscore.core.flowable import Flowable
from neoscore.core.staff import Staff
from neoscore.models.beat import Beat
from neoscore.models.pitch import Pitch
from neoscore.models.vertical_direction import VerticalDirection
from neoscore.utils.point import Point
from neoscore.utils.units import Mm


from ..helpers import assert_almost_equal

# TODO LOW test that glyphs are actually created successfully - this
# failed to catch bugs in creating rhythm dots and flags, and probably
# fails to catch other similar ones too.


class TestChordrest(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.flowable = Flowable(Point(Mm(0), Mm(0)), Mm(10000), Mm(100))
        self.staff = Staff(Point(Mm(0), Mm(0)), Mm(100), self.flowable)
        Clef(self.staff, Mm(0), "treble")

    def test_ledger_line_positions(self):
        pitches = ["c'", "b'", "f'''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.ledger_line_positions == [
            self.staff.unit(5),
            self.staff.unit(-3),
            self.staff.unit(-2),
            self.staff.unit(-1),
        ]

    def test_ledger_line_positions_with_different_clef(self):
        Clef(self.staff, Mm(10), "bass")
        pitches = ["e,", "d", "e'"]
        chord = Chordrest(Mm(15), self.staff, pitches, Beat(1, 4))
        assert chord.ledger_line_positions == [
            self.staff.unit(5),
            self.staff.unit(-2),
            self.staff.unit(-1),
        ]

    def test_rhythm_dot_positions_with_rest(self):
        chord = Chordrest(Mm(1), self.staff, None, Beat(7, 16))
        dots = list(chord.rhythm_dot_positions)
        dots.sort(key=lambda d: d.x)
        assert_almost_equal(
            dots[0], Point(self.staff.unit(1.326), self.staff.unit(1.5))
        )
        assert_almost_equal(
            dots[1], Point(self.staff.unit(1.826), self.staff.unit(1.5))
        )

    def test_rhythm_dot_positions_with_noteheads(self):
        pitches = ["e,", "d", "e'''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(7, 16))
        dots = list(chord.rhythm_dot_positions)
        dots.sort(key=lambda d: d.x)
        dots.sort(key=lambda d: d.y)
        assert_almost_equal(
            dots[0], Point(self.staff.unit(1.43), self.staff.unit(-3.5))
        )
        assert_almost_equal(
            dots[1], Point(self.staff.unit(1.93), self.staff.unit(-3.5))
        )
        assert_almost_equal(dots[2], Point(self.staff.unit(1.43), self.staff.unit(7.5)))
        assert_almost_equal(dots[3], Point(self.staff.unit(1.93), self.staff.unit(7.5)))
        assert_almost_equal(
            dots[4], Point(self.staff.unit(1.43), self.staff.unit(10.5))
        )
        assert_almost_equal(
            dots[5], Point(self.staff.unit(1.93), self.staff.unit(10.5))
        )

    def test_furthest_notehead_with_one_note(self):
        pitches = ["b'"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.furthest_notehead.pitch == Pitch("b'")
        pitches = ["f'''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.furthest_notehead.pitch == Pitch("f'''")
        pitches = ["c,,,,"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.furthest_notehead.pitch == Pitch("c,,,,")

    def test_furthest_notehead_with_many_notes(self):
        pitches = ["b''", "bs'"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.furthest_notehead.pitch == Pitch("b''")
        pitches = ["b'", "b,,,"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.furthest_notehead.pitch == Pitch("b,,,")
        pitches = ["f''''", "b"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.furthest_notehead.pitch == Pitch("f''''")
        pitches = ["c'", "c,,,,", "b'", "c'''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.furthest_notehead.pitch == Pitch("c,,,,")

    def test_highest_notehead(self):
        pitches = ["c'", "b'", "c'''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.highest_notehead.pitch == Pitch("c'''")

    def test_lowest_notehead(self):
        pitches = ["c'", "b'", "c'''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.lowest_notehead.pitch == Pitch("c'")

    def test_highest_and_lowest_notehead_same_with_one_note(self):
        pitches = ["c'"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.highest_notehead == chord.lowest_notehead

    def test_stem_direction_down(self):
        pitches = ["c'", "b'", "c''''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.stem_direction == VerticalDirection.DOWN

    def test_stem_direction_up(self):
        pitches = ["c,,,,,", "b'", "c'''"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.stem_direction == VerticalDirection.UP

    def test_stem_direction_down_with_one_note_at_staff_center(self):
        pitches = ["b'"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert chord.stem_direction == VerticalDirection.DOWN

    def test_stem_direction_override(self):
        pitches = ["b'"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4), VerticalDirection.UP)
        assert chord.stem_direction == VerticalDirection.UP
        # Setting stem_direction = None should revert to default 1
        chord.stem_direction = None
        assert chord.stem_direction == VerticalDirection.DOWN

    def test_stem_height_min(self):
        pitches = ["b'"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert_almost_equal(chord.stem_height, self.staff.unit(3))

    def test_stem_height_fitted(self):
        pitches = ["c'''", "g"]
        chord = Chordrest(Mm(1), self.staff, pitches, Beat(1, 4))
        assert_almost_equal(chord.stem_height, self.staff.unit(-10.5))
