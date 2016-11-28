import unittest
from nose.tools import assert_raises

from brown.core import brown
from brown.core.paper import Paper
from brown.core.flowable_frame import FlowableFrame
from brown.primitives.staff import Staff
from brown.utils.point import Point
from brown.utils.staff_point import StaffPoint
from brown.utils.anchored_point import AnchoredPoint
from brown.utils.units import Unit, Mm, StaffUnit



class TestStaffPoint(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((0, 0), Mm(50), self.frame, staff_unit=Mm(1))

    def test_init_with_point(self):
        existing_point = Point((1, 2))
        point = StaffPoint(existing_point, self.staff)
        assert(point.x == 1)
        assert(isinstance(point.x, int))
        assert(point.y == StaffUnit(existing_point.y, self.staff))
        assert(isinstance(point.y, StaffUnit))

    def test_init_with_tuple(self):
        existing_tuple = (1, 2)
        point = StaffPoint(existing_tuple, self.staff)
        assert(point.x == 1)
        assert(isinstance(point.x, int))
        assert(point.y == StaffUnit(existing_tuple[1], self.staff))
        assert(isinstance(point.y, StaffUnit))

    def test_init_with_staff_unit(self):
        existing_tuple = (1, StaffUnit(2, self.staff))
        point = StaffPoint(existing_tuple, self.staff)
        assert(point.x == 1)
        assert(isinstance(point.x, int))
        assert(point.y == StaffUnit(existing_tuple[1], self.staff))
        assert(isinstance(point.y, StaffUnit))

    def test_init_with_mismatched_staves(self):
        other_staff = Staff((20, 30), Mm(50), self.frame, staff_unit=Mm(1))
        existing_tuple = (1, StaffUnit(2, other_staff))
        with assert_raises(ValueError):
            point = StaffPoint(existing_tuple, self.staff)
