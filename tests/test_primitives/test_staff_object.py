from nose.tools import assert_raises
import unittest

from brown.core import brown
from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject, NoAncestorStaffError
from brown.core.flowable_frame import FlowableFrame
from brown.core.paper import Paper
from brown.utils.units import Mm


class TestStaffObject(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_find_staff_with_direct_parent(self):
        class StaffObjectClass(StaffObject):
            pass
        staff = Staff((0, 0), 100, self.frame)
        child_object = StaffObjectClass((Mm(0), Mm(0)), Mm(5), staff)
        assert(child_object.staff == staff)

    def test_find_staff_with_ancestor(self):
        class ParentObject(StaffObject):
            pass

        class ChildObject(StaffObject):
            pass
        staff = Staff((0, 0), 100, self.frame)
        parent_object = ParentObject((Mm(0), Mm(0)), Mm(5), staff)
        child_object = ChildObject((Mm(10), Mm(1)), Mm(5), parent_object)
        assert(child_object.staff == staff)

    @unittest.skip
    def test_find_staff_with_no_staff_raises_error(self):
        # TODO: Implement this test once this functionality is locked down
        pass
