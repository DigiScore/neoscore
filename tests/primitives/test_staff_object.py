import pytest

from brown.core import brown
from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject


def test_find_ancestor_staff_with_direct_parent():


    class ChildObject(StaffObject):
        pass

    test_staff = Staff(0, 0, 100)
    test_child_object = ChildObject(test_staff, 0)
    # TODO: Once proper parentage is implemented, this parent shouldn't have to
    #       be set manually
    test_child_object.parent = test_staff

    assert(test_child_object._find_ancestor_staff() == test_staff)
