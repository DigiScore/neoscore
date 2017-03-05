from brown.core.music_text_object import MusicTextObject
from brown.core.staff_object import StaffObject


class MockStaffObject(MusicTextObject, StaffObject):
    def __init__(self, pos, parent):
        MusicTextObject.__init__(self, pos, 'accidentalFlat', parent)
        StaffObject.__init__(self, parent)
