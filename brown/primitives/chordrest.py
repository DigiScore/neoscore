from brown.primitives.notehead import Notehead
from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject
from brown.primitives.ledger_line import LedgerLine


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
        self._ledgers = []
        for item in noteheads:
            self._noteheads.append(Notehead(self.staff, self.position_x, item))
            # TODO: quick hack
            self._noteheads[-1].grob.x -= self._noteheads[-1].grob_width
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
    def ledgers(self):
        """list [LedgerLine]: The ledger lines contained in this ChordRest.

        An empty list means no ledgers.
        """
        return self._ledgers

    @ledgers.setter
    def ledgers(self, value):
        self._ledgers = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    ######## PRIVATE PROPERTIES ########

    @property
    def _ledger_line_positions(self):
        """set[int]: A set of staff positions of needed ledger lines.

        Positions are in centered staff positions.

        An empty set means no ledger lines are needed
        """
        return {note.staff_position for note in self.noteheads
                if self.staff._position_needs_ledger(note.staff_position)}

    ######## PUBLIC METHODS ########

    def render(self):
        # TODO: render stem
        for note in self.noteheads:
            note.render()
        # Generate and render ledger lines
        self._create_ledgers()
        for ledger in self.ledgers:
            ledger.render()

    ######## PRIVATE METHODS ########

    def _create_ledgers(self):
        """Create all required ledger lines and store them in `self.ledgers`

        Returns: None

        Warning: This overwrites the contents of `self.ledgers`

        """
        self.ledgers = []
        for ledger_pos in self._ledger_line_positions:
            print('adding ledger at position')
            self.ledgers.append(
                LedgerLine(self.staff, self.position_x, ledger_pos)
            )
