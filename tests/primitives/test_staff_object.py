import pytest
from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject, NoAncestorStaffError


def test_find_root_staff_with_direct_parent():

    class ChildObject(StaffObject):
        pass

    test_staff = Staff(0, 0, 100)
    test_child_object = ChildObject(test_staff, 0)
    assert(test_child_object.root_staff == test_staff)


def test_find_root_staff_with_ancestor():

    class ParentObject(StaffObject):
        pass

    class ChildObject(StaffObject):
        pass

    test_staff = Staff(0, 0, 100)
    test_parent_object = ParentObject(test_staff, 0)
    test_child_object = ChildObject(test_parent_object, 50)

    assert(test_child_object.root_staff == test_staff)


def test_find_root_staff_with_no_staf_raises_error():

    class ChildObject(StaffObject):
        pass

    with pytest.raises(NoAncestorStaffError):
        ChildObject(None, 0)
