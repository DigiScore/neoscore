import unittest

from neoscore.core import neoscore
from neoscore.core.directions import VerticalDirection
from neoscore.core.flowable import Flowable
from neoscore.core.units import Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.duration import Duration
from neoscore.western.staff import Staff
from neoscore.western.stem import Stem


class TestStem(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))

    def test_stem_direction(self):
        stem = Stem((Mm(0), Mm(0)), self.staff, VerticalDirection.UP, Mm(10))
        assert stem.direction == VerticalDirection.UP
        assert stem.direction.value == -1

        stem = Stem((Mm(0), Mm(0)), self.staff, VerticalDirection.DOWN, Mm(10))
        assert stem.direction == VerticalDirection.DOWN
        assert stem.direction.value == 1

    def test_stem_direction_in_chordrest(self):
        Clef(Mm(0), self.staff, "treble")
        note_list = [
            ("c,", VerticalDirection.UP),
            ("c", VerticalDirection.UP),
            ("c'", VerticalDirection.UP),
            ("g'", VerticalDirection.UP),
            ("c''", VerticalDirection.DOWN),
            ("gx'", VerticalDirection.UP),
            ("gx'''", VerticalDirection.DOWN),
        ]
        for note, direction in note_list:
            chord = Chordrest(Mm(15), self.staff, [note], Duration(1, 4))
            assert chord.stem_direction == direction
