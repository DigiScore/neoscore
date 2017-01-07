import unittest

from brown.core import brown
from brown.primitives.staff import Staff
from brown.primitives.chordrest import ChordRest
from brown.primitives.clef import Clef
from brown.models.pitch import Pitch
from brown.utils.units import Mm
from brown.utils.point import Point


class TestChordRest(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.staff = Staff(Point(Mm(0), Mm(0)), Mm(100), None)
        self.clef = Clef(self.staff, Mm(0), 'treble')

    def test_ledger_line_positions(self):
        pitches = ["c'", "b'", "f'''"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.ledger_line_positions ==
               {self.staff.unit(5), self.staff.unit(-1),
                self.staff.unit(-2), self.staff.unit(-3)})

    def test_ledger_line_positions_with_different_clef(self):
        clef = Clef(self.staff, Mm(0), 'bass')
        pitches = ["e,", "d", "e'"]
        chord = ChordRest(Mm(10), self.staff, pitches)
        assert(chord.ledger_line_positions ==
               {self.staff.unit(5), self.staff.unit(-1), self.staff.unit(-2)})

    def test_furthest_notehead_with_one_note(self):
        pitches = ["b'"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.furthest_notehead.pitch == Pitch("b'"))
        pitches = ["f'''"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.furthest_notehead.pitch == Pitch("f'''"))
        pitches = ["c,,,,"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.furthest_notehead.pitch == Pitch("c,,,,"))

    def test_furthest_notehead_with_many_notes(self):
        pitches = ["b'", "b,,,"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.furthest_notehead.pitch == Pitch("b,,,"))
        pitches = ["f''''", "b"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.furthest_notehead.pitch == Pitch("f''''"))
        pitches = ["c'", "c,,,,", "b'", "c'''"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.furthest_notehead.pitch == Pitch("c,,,,"))

    def test_highest_notehead(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.highest_notehead.pitch == Pitch("c'''"))

    def test_lowest_notehead(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.lowest_notehead.pitch == Pitch("c'"))

    def test_highest_and_lowest_notehead_same_with_one_note(self):
        pitches = ["c'"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.highest_notehead == chord.lowest_notehead)

    def test_stem_direction_down(self):
        pitches = ["c'", "b'", "c''''"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.stem_direction == 1)

    def test_stem_direction_up(self):
        pitches = ["c,,,,,", "b'", "c'''"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.stem_direction == -1)

    def test_stem_direction_down_with_one_note_at_staff_center(self):
        pitches = ["b'"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.stem_direction == 1)

    def test_stem_height_min(self):
        pitches = ["b'"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        assert(chord.stem_height == self.staff.unit(5))

    def test_stem_height_fitted(self):
        pitches = ["c'''", "g"]
        chord = ChordRest(Mm(1), self.staff, pitches)
        self.assertAlmostEqual(self.staff.unit(chord.stem_height).value,
                               self.staff.unit(-10.5).value)
