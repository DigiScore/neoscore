import unittest

from brown.core import brown
from brown.core.staff import Staff
from brown.models.pitch import Pitch
from brown.primitives.chordrest import ChordRest
from brown.utils.point import Point
from brown.utils.units import Mm


class TestChordRest(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.staff = Staff(Point(Mm(0), Mm(0)), Mm(100), None)
        self.staff.add_clef((0, 1), 'treble')

    def test_ledger_line_positions(self):
        pitches = ["c'", "b'", "f'''"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.ledger_line_positions ==
               {self.staff.unit(5), self.staff.unit(-1),
                self.staff.unit(-2), self.staff.unit(-3)})

    def test_ledger_line_positions_with_different_clef(self):
        self.staff.add_clef((1, 4), 'bass')
        pitches = ["e,", "d", "e'"]
        chord = ChordRest(self.staff.beat(2, 4),
                          self.staff,
                          pitches,
                          self.staff.beat(1, 4))
        assert(chord.ledger_line_positions ==
               {self.staff.unit(5), self.staff.unit(-1), self.staff.unit(-2)})

    def test_rhythm_dot_positions_with_rest(self):
        chord = ChordRest(Mm(1), self.staff, None, self.staff.beat(7, 16))
        dots = set(chord.rhythm_dot_positions)
        assert(dots == {
            Point(self.staff.unit(1.076), self.staff.unit(1.5)),
            Point(self.staff.unit(1.576), self.staff.unit(1.5)),
        })

    def test_rhythm_dot_positions_with_noteheads(self):
        pitches = ["e,", "d", "e'''"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(7, 16))
        dots = set(chord.rhythm_dot_positions)
        assert(dots == {
            Point(self.staff.unit(1.18), self.staff.unit(-3.5)),
            Point(self.staff.unit(1.68), self.staff.unit(-3.5)),
            Point(self.staff.unit(1.18), self.staff.unit(7.5)),
            Point(self.staff.unit(1.68), self.staff.unit(7.5)),
            Point(self.staff.unit(1.18), self.staff.unit(10.5)),
            Point(self.staff.unit(1.68), self.staff.unit(10.5)),
        })

    def test_furthest_notehead_with_one_note(self):
        pitches = ["b'"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.furthest_notehead.pitch == Pitch("b'"))
        pitches = ["f'''"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.furthest_notehead.pitch == Pitch("f'''"))
        pitches = ["c,,,,"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.furthest_notehead.pitch == Pitch("c,,,,"))

    def test_furthest_notehead_with_many_notes(self):
        pitches = ["b'", "b,,,"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.furthest_notehead.pitch == Pitch("b,,,"))
        pitches = ["f''''", "b"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.furthest_notehead.pitch == Pitch("f''''"))
        pitches = ["c'", "c,,,,", "b'", "c'''"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.furthest_notehead.pitch == Pitch("c,,,,"))

    def test_highest_notehead(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.highest_notehead.pitch == Pitch("c'''"))

    def test_lowest_notehead(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.lowest_notehead.pitch == Pitch("c'"))

    def test_highest_and_lowest_notehead_same_with_one_note(self):
        pitches = ["c'"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.highest_notehead == chord.lowest_notehead)

    def test_stem_direction_down(self):
        pitches = ["c'", "b'", "c''''"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.stem_direction == 1)

    def test_stem_direction_up(self):
        pitches = ["c,,,,,", "b'", "c'''"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.stem_direction == -1)

    def test_stem_direction_down_with_one_note_at_staff_center(self):
        pitches = ["b'"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.stem_direction == 1)

    def test_stem_height_min(self):
        pitches = ["b'"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        assert(chord.stem_height == self.staff.unit(5))

    def test_stem_height_fitted(self):
        pitches = ["c'''", "g"]
        chord = ChordRest(Mm(1), self.staff, pitches, self.staff.beat(1, 4))
        self.assertAlmostEqual(self.staff.unit(chord.stem_height).value,
                               self.staff.unit(-10.5).value)
