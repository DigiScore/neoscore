import unittest

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.utils.point import Point
from neoscore.utils.units import Mm
from neoscore.western.stem import Stem
from neoscore.western.staff import Staff


class TestStem(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))


    def test_stem_direction(self):
        # bar_line = BarLine(Mm(15), [self.staff_1, self.staff_2])
        stem = Stem((Mm(0), Mm(0)), self.staff, 1, Mm(10))
        assert stem.pos == Point(Mm(0), Mm(0))
        assert stem.direction == 1


        assert bar_line.elements[0].pos == Point(Mm(0), Mm(0))
        assert bar_line.elements[0].parent == bar_line
        assert bar_line.elements[1].pos == Point(Mm(15), self.staff_2.height)
        assert bar_line.elements[1].parent == self.staff_2
