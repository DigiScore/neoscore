from nose.tools import assert_raises
import unittest

from brown.core import brown
from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject, NoAncestorStaffError
from brown.core.music_glyph import MusicGlyph
from brown.core.flowable_frame import FlowableFrame
from brown.core.paper import Paper
from brown.utils.units import Mm


class MockStaffObject(MusicGlyph, StaffObject):
    def __init__(self, pos, parent):
        MusicGlyph.__init__(self, pos, 'accidentalFlat', parent=parent)
        StaffObject.__init__(self, parent)


class TestStaffObject(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)

    def test_find_staff_with_direct_parent(self):
        child_object = MockStaffObject((Mm(0), Mm(0)), self.staff)
        assert(child_object.staff == self.staff)

    def test_find_staff_with_ancestor(self):
        class ParentObject(MockStaffObject):
            pass
        class ChildObject(MockStaffObject):
            pass
        parent_object = ParentObject((Mm(0), Mm(0)), self.staff)
        child_object = ChildObject((Mm(10), Mm(1)), parent_object)
        assert(child_object.staff == self.staff)

    @unittest.skip
    def test_find_staff_with_no_staff_raises_error(self):
        # TODO: Implement this test once this functionality is locked down
        pass
