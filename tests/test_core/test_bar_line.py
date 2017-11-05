import unittest

from brown.core import brown
from brown.core.bar_line import BarLine
from brown.core.flowable import Flowable
from brown.core.staff import Staff
from brown.utils.point import Point
from brown.utils.units import Mm


class TestBarLine(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff_1 = Staff((Mm(0), Mm(0)), Mm(100), self.flowable)
        self.staff_2 = Staff((Mm(0), Mm(30)), Mm(100), self.flowable)
        self.staff_3 = Staff((Mm(10), Mm(50)), Mm(100), self.flowable)

    def test_path_shape_with_same_staff_x_coords(self):
        bar_line = BarLine(Mm(15), [self.staff_1, self.staff_2])
        assert(bar_line.elements[0].pos == Point(Mm(0), Mm(0)))
        assert(bar_line.elements[0].parent == bar_line)
        assert(bar_line.elements[1].pos == Point(Mm(15), self.staff_2.height))
        assert(bar_line.elements[1].parent == self.staff_2)

    def test_path_shape_with_different_staff_x_coords(self):
        bar_line = BarLine(Mm(15), [self.staff_1, self.staff_2, self.staff_3])
        assert(bar_line.elements[0].pos == Point(Mm(0), Mm(0)))
        assert(bar_line.elements[0].parent == bar_line)
        assert(bar_line.elements[1].pos == Point(Mm(5), self.staff_3.height))
        assert(bar_line.elements[1].parent == self.staff_3)
