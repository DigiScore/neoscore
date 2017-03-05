from brown.core.music_text import MusicText
from brown.core.staff_object import StaffObject


class MockStaffObject(MusicText, StaffObject):
    def __init__(self, pos, parent):
        MusicText.__init__(self, pos, 'accidentalFlat', parent)
        StaffObject.__init__(self, parent)
