from brown.core.invisible_object import InvisibleObject
from brown.core.staff_object import StaffObject


class MockStaffObject(InvisibleObject, StaffObject):
    def __init__(self, pos, parent):
        InvisibleObject.__init__(self, pos, parent)
        StaffObject.__init__(self, parent)
