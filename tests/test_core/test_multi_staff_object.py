import unittest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.multi_staff_object import MultiStaffObject
from brown.core.staff import Staff
from brown.utils.units import Mm

from ..helpers import assert_almost_equal


class TestMultiStaffObject(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff_1 = Staff((Mm(0), Mm(0)), Mm(100), self.flowable)
        self.staff_2 = Staff((Mm(0), Mm(30)), Mm(100), self.flowable)
        self.staff_3 = Staff((Mm(0), Mm(50)), Mm(100), self.flowable)

    def test_visually_sorted_staves(self):
        multi_object = MultiStaffObject({self.staff_1, self.staff_2, self.staff_3})
        assert multi_object.visually_sorted_staves == [
            self.staff_1,
            self.staff_2,
            self.staff_3,
        ]

    def test_highest_staff(self):
        multi_object = MultiStaffObject({self.staff_1, self.staff_2, self.staff_3})
        assert multi_object.highest_staff == self.staff_1

    def test_lowest_staff(self):
        multi_object = MultiStaffObject({self.staff_1, self.staff_2, self.staff_3})
        assert multi_object.lowest_staff == self.staff_3

    def test_vertical_span(self):
        multi_object = MultiStaffObject({self.staff_1, self.staff_2, self.staff_3})
        assert_almost_equal(multi_object.vertical_span, self.staff_3.unit(4) + Mm(50))
