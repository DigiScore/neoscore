from neoscore.core.directions import VerticalDirection
from neoscore.core.flowable import Flowable
from neoscore.core.units import Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.duration import Duration
from neoscore.western.octave_line import OctaveLine
from neoscore.western.staff import Staff
from neoscore.western.stem import Stem

from ..helpers import AppTest


class TestStem(AppTest):
    def setUp(self):
        super().setUp()
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
        for n, (note, direction) in enumerate(note_list):
            chord = Chordrest(Mm(15 + n), self.staff, [note], Duration(1, 4))
            assert chord.stem_direction == direction

    def test_stem_direction_in_dyads_and_low_staffs(self):
        Clef(Mm(0), self.staff, "treble")
        lowest_staff = Staff((Mm(10), Mm(18)), self.flowable, Mm(2000), Mm(1))
        Clef(Mm(0), lowest_staff, "bass")
        OctaveLine(
            (Mm(20), self.staff.unit(-2)), self.staff, Mm(1000), indication="8vb"
        )

        assert (
            Chordrest(Mm(10), self.staff, ["a'", "bs"], Duration(2, 4)).stem_direction
            == VerticalDirection.UP
        )
        assert (
            Chordrest(Mm(15), self.staff, ["b'", "bff"], Duration(2, 4)).stem_direction
            == VerticalDirection.UP
        )
        assert (
            Chordrest(Mm(40), self.staff, ["a'", "b'"], Duration(2, 4)).stem_direction
            == VerticalDirection.DOWN
        )
        assert (
            Chordrest(Mm(60), self.staff, ["b'", "bff"], Duration(2, 4)).stem_direction
            == VerticalDirection.DOWN
        )

        assert (
            Chordrest(
                Mm(10),
                lowest_staff,
                [("a", "accidentalQuarterToneSharpStein", 2)],
                (3, 4),
            ).stem_direction
            == VerticalDirection.UP
        )
        assert (
            Chordrest(
                Mm(15),
                lowest_staff,
                [("a", "accidentalFlatRepeatedSpaceStockhausen", 2)],
                (3, 16),
            ).stem_direction
            == VerticalDirection.UP
        )
