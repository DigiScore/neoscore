from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject

# ?
from brown.models.transposition import Transposition
from brown.models.clef import Clef
from brown.models.pitch import Pitch  # ?
from brown.models.duration import Duration
from brown.models.position import Position


"""

Thoughts----

how to render?

should only directly interact with primitives and core, never interface

utils/object models allowed

"""


class ChordRest(StaffObject):
    def __init__(staff, noteheads, duration, position):
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
    def noteheads():
        return self._noteheads

    @noteheads.setter
    def noteheads(value):
        self._noteheads = value

    @property
    def duration():
        return self._duration

    @duration.setter
    def duration(value):
        self._duration = value

    @property
    def position():
        return self._position

    @position.setter
    def position(value):
        self._position = value

    def draw():
        pass
