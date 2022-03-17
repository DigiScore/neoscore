from neoscore.core.positioned_object import PositionedObject
from neoscore.western.staff_object import StaffObject


class MockStaffObject(PositionedObject, StaffObject):
    def __init__(self, pos, parent):
        PositionedObject.__init__(self, pos, parent)
        StaffObject.__init__(self, parent)
