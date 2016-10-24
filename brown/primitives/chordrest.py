from brown.primitives.notehead import Notehead
from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject


class ChordRest(StaffObject):
    # (use temporary None in duration until those are implemented)
    def __init__(self, staff, noteheads, position_x, duration=None):
        '''
        Args:
            staff (Staff): The parent staff
            noteheads (list[Notehead]): A list of pitch strings
                representing noteheads. An empty list indicates a rest.
            duration (Duration): A duration value for the chord
        '''
        super(ChordRest, self).__init__(staff, position_x)
        self._noteheads = []
        for item in noteheads:
            self._noteheads.append(Notehead(self.staff, self.position_x, item))
        self._duration = duration

    ######## PUBLIC PROPERTIES ########

    @property
    def noteheads(self):
        """list [Notehead]: The noteheads contained in this ChordRest.

        An empty list means a rest.
        """
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

    def render(self):
        # TODO: render stem and ledger lines too
        for note in self.noteheads:
            note.render()
