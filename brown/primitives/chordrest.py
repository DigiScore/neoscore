from brown.utils.units import GraphicUnit, Mm
from brown.primitives.notehead import Notehead
from brown.primitives.accidental import Accidental
from brown.primitives.staff_object import StaffObject
from brown.primitives.ledger_line import LedgerLine
from brown.primitives.stem import Stem
from brown.core.object_group import ObjectGroup
from brown.utils.point import Point


class ChordRest(ObjectGroup, StaffObject):
    # (use temporary None in duration until those are implemented)
    def __init__(self, pos_x, staff, noteheads=None, duration=None):
        '''
        Args:
            pos_x (Unit): The horizontal position of the ChordRest
            staff (Staff): The staff the object is attached to
            noteheads (list[Notehead]): A list of pitch strings
                representing noteheads. An empty list indicates a rest.
            duration (Duration): The duration of the ChordRest
        '''
        ObjectGroup.__init__(self, Point(pos_x, staff.unit(0)), staff, None)
        StaffObject.__init__(self, staff)
        for pitch in noteheads:
            self.register_object(Notehead(staff.unit(0), pitch, self))
        self._duration = duration
        self._stem = None

    ######## PUBLIC PROPERTIES ########

    @property
    def noteheads(self):
        """iter(Notehead): The noteheads contained in this ChordRest."""
        return (item for item in self.objects if isinstance(item, Notehead))

    @property
    def accidentals(self):
        """iter(Accidental): The accidentals contained in this ChordRest."""
        return (item for item in self.objects if isinstance(item, Accidental))

    @property
    def ledgers(self):
        """iter(LedgerLine): The ledger lines contained in this ChordRest.

        An empty list means no ledgers.
        """
        return (item for item in self.objects if isinstance(item, LedgerLine))

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
    def leftmost_notehead(self):
        """Notehead or None: the Notehead furthest to the left in the chord"""
        return min(self.noteheads,
                   key=lambda n: n.position_x,
                   default=None)

    @property
    def rightmost_notehead(self):
        """Notehead or None: the Notehead furthest to the right in the chord"""
        return max(self.noteheads,
                   key=lambda n: n.position_x,
                   default=None)

    @property
    def widest_notehead(self):
        """Notehead or None: the Notehead with the greatest `visual_width`"""
        return max(self.noteheads,
                   key=lambda n: n.visual_width,
                   default=None)

    @property
    def notehead_column_width(self):
        """Unit: The total width of all Noteheads in the chord"""
        if not self.noteheads:
            return 0
        elif len(self.noteheads) == 1:
            return self.widest_notehead.visual_width
        else:
            return (self.rightmost_notehead.position_x -
                    self.leftmost_notehead.position_x +
                    self.widest_notehead.visual_width)

    @property
    def noteheads_outside_staff(self):
        """set{Notehead}: All noteheads which are above or below the staff"""
        return set(note for note in self.noteheads
                   if self.staff._position_outside_staff(note.staff_position))

    @property
    def leftmost_notehead_outside_staff(self):
        """Notehead or None: the Notehead furthest to the left outside the staff"""
        return min(self.noteheads_outside_staff,
                   key=lambda n: n.position_x,
                   default=None)

    @property
    def rightmost_notehead_outside_staff(self):
        """Notehead or None: the Notehead furthest to the right outside the staff"""
        return max(self.noteheads_outside_staff,
                   key=lambda n: n.position_x,
                   default=None)

    @property
    def notehead_column_outside_staff_width(self):
        """Unit: The total width of any noteheads outside the staff"""
        if not self.noteheads:
            return 0
        elif len(self.noteheads) == 1:
            return self.widest_notehead.visual_width
        else:
            return (self.rightmost_notehead_outside_staff.position_x -
                    self.leftmost_notehead_outside_staff.position_x +
                    self.widest_notehead.visual_width)

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
        # Position noteheads and accidentals
        self._position_noteheads_horizontally()
        self._position_accidentals_horizontally()
        # Generate non-notehead group members
        self._create_accidentals()
        #self._create_ledgers()
        #self._create_stem()
        super().render()

    ######## PRIVATE METHODS ########

    def _create_ledgers(self):
        """Create all required ledger lines and store them in `self.ledgers`

        Returns: None

        Warning: This should be called after _position_noteheads_horizontally()
                 as it relies on the position of noteheads in the chord to
                 calculate the position and length of the ledger lines
        Warning: This overwrites the contents of `self.ledgers`
        """
        # Calculate x position and length of ledger lines
        x_position = self.leftmost_notehead.position_x - (0.3 * self.staff.staff_unit)
        length = self.notehead_column_outside_staff_width + (0.6 * self.staff.staff_unit)
        # Flush any existing ledgers:
        self._objects = set(item for item in self.objects
                            if not isinstance(item, LedgerLine))
        for staff_pos in self.ledger_line_positions:
            self.register_object(
                LedgerLine(self, x_position, staff_pos, length))

    def _create_accidentals(self):
        """TODO"""
        pass

    def _create_stem(self):
        """Creates a Stem and stores it in `self.stem`.

        Returns: None
        """
        start = self.furthest_notehead.staff_position
        end = start + self.stem_direction * 6
        self._stem = Stem(self, 0, start, end)

    def _position_noteheads_horizontally(self):
        """Reposition noteheads so that they are laid out correctly

        Decides which noteheads lie on which side of the staff, and
        modifies positions when needed by directly changing the grobs'
        `position_x` properties.

        Returns: None
        """
        # Find the preferred side of the stem for noteheads,
        # where 1 means right and -1 means left
        default_side = self.stem_direction * -1
        # Start last staff pos at sentinel infinity position
        prev_staff_pos = self.staff.unit(float("inf"))
        # Start prev_side at wrong side so first note goes on the default side
        prev_side = -1 * default_side
        for note in sorted(self.noteheads,
                           key=lambda n: n.staff_position,
                           reverse=(self.stem_direction == -1)):
            if abs(prev_staff_pos - note.staff_position) < 2:
                # This note collides with previous, use switch sides
                prev_side = -1 * prev_side
            else:
                prev_side = default_side
            # Reposition, using prev_side (here) as the chosen side for this note
            if prev_side == -1:
                note.position_x -= note.visual_width
            # Lastly, update prev_staff_pos
            prev_staff_pos = note.staff_position

    def _position_accidentals_horizontally(self):
        """Reposition accidentals so that they are laid out correctly

        TODO: Implement me

        Returns: None
        """
        pass
