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

