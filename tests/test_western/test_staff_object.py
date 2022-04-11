import pytest

from neoscore.core import neoscore
from neoscore.core.exceptions import NoAncestorStaffError
from neoscore.core.flowable import Flowable
from neoscore.core.paper import Paper
from neoscore.core.units import Mm
from neoscore.western.staff import Staff
from tests.mocks.mock_staff_object import MockStaffObject

from ..helpers import AppTest


class TestStaffObject(AppTest):
    def setUp(self):
        super().setUp()
        neoscore.document.paper = Paper(
            *[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]
        )
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(5000))

    def test_find_staff_with_direct_parent(self):
        child_object = MockStaffObject((Mm(0), Mm(0)), self.staff)
        assert child_object.staff == self.staff

    def test_find_staff_with_ancestor(self):
        parent_object = MockStaffObject((Mm(0), Mm(0)), self.staff)
        child_object = MockStaffObject((Mm(10), Mm(1)), parent_object)
        assert child_object.staff == self.staff

    def test_find_staff_with_no_staff_raises_error(self):
        with pytest.raises(NoAncestorStaffError):
            MockStaffObject((Mm(0), Mm(0)), neoscore.document.pages[0])

    def test_pos_in_staff(self):
        test_object = MockStaffObject((Mm(5000), Mm(0)), self.staff)
        assert test_object.pos_in_staff == test_object.pos

    def test_pos_x_in_staff(self):
        test_object = MockStaffObject((Mm(5000), Mm(0)), self.staff)
        assert test_object.pos_x_in_staff == test_object.x

    def test_pos_in_staff_with_indirect_ancestor_staff(self):
        parent_object = MockStaffObject((Mm(1), Mm(2)), self.staff)
        test_object = MockStaffObject((Mm(10), Mm(1)), parent_object)
        pos_in_staff = test_object.pos_in_staff
        self.assertAlmostEqual(Mm(pos_in_staff.x).display_value, 11)
        self.assertAlmostEqual(Mm(pos_in_staff.y).display_value, 3)
