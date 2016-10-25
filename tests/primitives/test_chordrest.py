import unittest
from brown.core import brown
from brown.primitives.notehead import Notehead
from brown.primitives.staff import Staff
from brown.primitives.chordrest import ChordRest
from brown.primitives.ledger_line import LedgerLine
from brown.primitives.stem import Stem
from brown.primitives.clef import Clef


class TestChordRest(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.mock_staff = Staff(0, 0, 100)

    def test_ledger_line_positions_treble(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.ledger_line_positions == {-6, 6, 8})

    def test_ledger_line_positions_bass(self):
        pitches = ["e,", "d", "g'"]
        clef = Clef(self.mock_staff, 0, 'bass')
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.ledger_line_positions == {-6, 6, 8, 10})

    def test_ledgers_empty_after_init(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.ledgers == [])

    def test_furthest_notehead_with_one_note_treble(self):
        pitches = ["b'"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.furthest_notehead == chord.noteheads[-1])
        pitches = ["f'''"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.furthest_notehead == chord.noteheads[-1])
        pitches = ["c,,,,"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.furthest_notehead == chord.noteheads[-1])

    def test_furthest_notehead_with_many_notes_treble(self):
        pitches = ["b'", "b,,,"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.furthest_notehead == chord.noteheads[-1])
        pitches = ["f''''", "b"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.furthest_notehead == chord.noteheads[0])
        pitches = ["c'", "c,,,,", "b'", "c'''"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.furthest_notehead == chord.noteheads[1])

    def test_highest_notehead(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.highest_notehead == chord.noteheads[-1])

    def test_lowest_notehead(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.lowest_notehead == chord.noteheads[0])

    def test_highest_and_lowest_notehead_same_with_one_note(self):
        pitches = ["c'"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.highest_notehead == chord.lowest_notehead)

    def test_stem_direction_down(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.stem_direction == -1)

    def test_stem_direction_up(self):
        pitches = ["c,,,,,", "b'", "c'''"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.stem_direction == 1)

    def test_stem_direction_down_when_one_note_at_staff_center(self):
        pitches = ["b'"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.stem_direction == -1)
