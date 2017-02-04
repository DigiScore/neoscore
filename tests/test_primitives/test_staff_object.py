import unittest

from brown.core import brown
from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject
from brown.core.music_text_object import MusicTextObject
from brown.core.flowable_frame import FlowableFrame
from brown.core.paper import Paper
from brown.utils.units import Mm
from brown.utils.point import Point


class MockStaffObject(MusicTextObject, StaffObject):
    def __init__(self, pos, parent):
        MusicTextObject.__init__(self, pos, 'accidentalFlat', parent)
        StaffObject.__init__(self, parent)


class TestStaffObject(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(5000), self.frame)

    def test_find_staff_with_direct_parent(self):
        child_object = MockStaffObject((Mm(0), Mm(0)), self.staff)
        assert(child_object.staff == self.staff)

    def test_find_staff_with_ancestor(self):
        parent_object = MockStaffObject((Mm(0), Mm(0)), self.staff)
        child_object = MockStaffObject((Mm(10), Mm(1)), parent_object)
        assert(child_object.staff == self.staff)

    @unittest.skip
    def test_find_staff_with_no_staff_raises_error(self):
        # TODO: Implement this test once this functionality is locked down
        pass

    def test_map_to_staff_unflowed(self):
        test_object = MockStaffObject((Mm(5000), Mm(0)), self.staff)
        assert(test_object.map_to_staff_unflowed() == test_object.pos)

    def test_find_staff_with_indirect_ancestor_staff(self):
        parent_object = MockStaffObject((Mm(1), Mm(2)), self.staff)
        test_object = MockStaffObject((Mm(10), Mm(1)), parent_object)
        assert(test_object.map_to_staff_unflowed() == Point(Mm(11), Mm(3)))
