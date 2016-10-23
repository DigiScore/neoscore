from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject



"""

Thoughts----

how to render?

should only directly interact with primitives and core, never interface

utils/object models allowed

"""


class ChordRest(StaffObject):
    def __init__(self, staff, noteheads, duration, position):
        '''
        Args:
            staff (Staff): The parent staff
            noteheads (list[Notehead]): A list of noteheads in the chordrest.
                An empty list indicates a rest.
            duration (Duration): A duration value for the chord
        '''
        self.staff = staff
        self.noteheads = noteheads
        self.duration = duration
        self.position = position

    @property
    def noteheads(self, ):
        return self._noteheads

    @noteheads.setter
    def noteheads(self, value):
        self._noteheads = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def draw(self):
        pass
