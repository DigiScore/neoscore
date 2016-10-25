from brown.primitives.notehead import Notehead
from brown.primitives.staff import Staff
from brown.primitives.staff_object import StaffObject
from brown.primitives.ledger_line import LedgerLine
from brown.primitives.stem import Stem


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
        for pitch in noteheads:
            self._noteheads.append(Notehead(self.staff,
                                            self.position_x,
                                            pitch))
        self._duration = duration
        self._stem = None

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
        """list[LedgerLine]: The ledger lines contained in this ChordRest.

        An empty list means no ledgers.
        """
        return self._ledgers

    @ledgers.setter
    def ledgers(self, value):
        self._ledgers = value

    @property
    def stem(self):
        """Stem: The Stem for the ChordRest."""
        return self._stem

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def ledger_line_positions(self):
        """set{int}: A set of staff positions of needed ledger lines.

        Positions are in centered staff positions.

        An empty set means no ledger lines are needed
        """
        highest = self.highest_notehead.staff_position
        lowest = self.lowest_notehead.staff_position
        # Join sets of needed ledgers above and below with union operator
        return (self.staff._ledgers_needed_from_position(lowest) |
                self.staff._ledgers_needed_from_position(highest))

    @property
    def furthest_notehead(self):
        """Notehead or None: The Notehead furthest from the staff center"""
        return max(self.noteheads,
                   key=lambda n: abs(n.staff_position),
                   default=None)

    @property
    def highest_notehead(self):
        """Notehead of None: The highest Notehead in the chord."""
        return max(self.noteheads,
                   key=lambda n: n.staff_position,
                   default=None)

    @property
    def lowest_notehead(self):
        """Notehead of None: The lowest Notehead in the chord."""
        return min(self.noteheads,
                   key=lambda n: n.staff_position,
                   default=None)

    @property
    def stem_direction(self):
        """int: The direction of the stem, either 1 (up) or -1 (down)

        Takes the notehead furthest from the center of the staff,
        and returns the opposite direction.

        If the furthest is at position 0, default to -1.
        """
        furthest = self.furthest_notehead
        if furthest:
            return 1 if furthest.staff_position < 0 else -1
        else:
            return None

    ######## PUBLIC METHODS ########

    def render(self):
        for note in self.noteheads:
            note.render()
        # Generate and render ledger lines
        self._create_ledgers()
        for ledger in self.ledgers:
            ledger.render()
        # Generate and render stem
        self._create_stem()
        self.stem.render()

    ######## PRIVATE METHODS ########

    def _create_ledgers(self):
        """Create all required ledger lines and store them in `self.ledgers`

        Returns: None

        Warning: This overwrites the contents of `self.ledgers`
        """
        self.ledgers = []
        for ledger_pos in self.ledger_line_positions:
            self.ledgers.append(
                LedgerLine(self.staff, self.position_x, ledger_pos)
            )

    def _create_stem(self):
        """Creates a Stem and stores it in `self.stem`.

        Returns: None
        """
        start = self.furthest_notehead.staff_position
        end = start + self.stem_direction * 6
        self._stem = Stem(self.staff, self.position_x,
                          start, end)
