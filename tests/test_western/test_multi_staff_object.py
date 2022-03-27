import unittest

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.utils.units import Mm
from neoscore.western.multi_staff_object import MultiStaffObject
from neoscore.western.staff import Staff
from tests.helpers import assert_almost_equal


class TestMultiStaffObject(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff_1 = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        self.staff_2 = Staff((Mm(0), Mm(30)), self.flowable, Mm(100))
        self.staff_3 = Staff((Mm(0), Mm(50)), self.flowable, Mm(100))

    def test_init_with_single_staff(self):
        multi_object = MultiStaffObject(self.staff_1)
        assert multi_object.staves == {self.staff_1}

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
