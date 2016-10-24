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

    def test_ledger_line_positions(self):
        pitches = ["c'", "b'", "c'''"]
        chord = ChordRest(self.mock_staff, pitches, 10)
        assert(chord.ledger_line_positions == {-6, 8})
