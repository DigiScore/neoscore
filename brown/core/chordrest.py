from brown.core.accidental import Accidental
from brown.core.flag import Flag
from brown.core.ledger_line import LedgerLine
from brown.core.notehead import Notehead
from brown.core.object_group import ObjectGroup
from brown.core.rest import Rest
from brown.core.rhythm_dot import RhythmDot
from brown.core.staff_object import StaffObject
from brown.core.stem import Stem
from brown.utils.point import Point


class Chordrest(ObjectGroup, StaffObject):

    """A chord or a rest.

    This is a general unified interface for conventionally notated
    musical notes/chords/rests. It can be given any number of pitches
    to be used as notes in the chord, or `None` for a rest.

    It will automatically generate and lay out:
        * `Notehead`s if pitches are given
        * a `Stem` if pitches are given and required by the given `Duration`
        * a `Flag` if pitches are given and required by the given `Duration`
        * `LedgerLine`s as needed (taking into consideration the given
          pitches and their location on the `Staff`)
        * `Accidental`s as needed by any given pitches
        * a `Rest` if no pitches are given
        * `RhythmDot`s if needed by the given `Duration`
    """

    def __init__(self, pos_x, staff, pitches, duration, stem_direction=None):
        """
        Args:
            pos_x (Unit): The horizontal position
            staff (Staff): The staff the object is attached to
            pitches (list[str] or None): A list of pitch strings
                representing noteheads. An empty list indicates a rest.
            duration (Beat): The duration of the Chordrest
            stem_direction (int or None): An optional stem direction override
                where `1` points down and `-1` points up. If omitted, the
                direction is automatically calculated to point away from
                the furthest-out notehead.
        """
        StaffObject.__init__(self, staff)
        ObjectGroup.__init__(self, Point(pos_x, staff.unit(0)), staff, None)
        self.duration = duration
        self._noteheads = set()
        self._accidentals = set()
        self._ledgers = set()
        self._stem_direction_override = stem_direction
        if pitches:
            for pitch in pitches:
                self._noteheads.add(
                    Notehead(staff.unit(0), pitch, self.duration, self))
            self.rest = None
        else:
            self.rest = Rest(staff.unit(0), self, duration)
        self._stem = None
        self._flag = None

    ######## PUBLIC PROPERTIES ########

    @property
    def noteheads(self):
        """set(Notehead): The noteheads contained in this Chordrest."""
        return self._noteheads

    @property
    def rest(self):
        """Rest or None: A Rest glyph, if no noteheads exist."""
        return self._rest

    @rest.setter
    def rest(self, value):
        self._rest = value

    @property
    def accidentals(self):
        """set(Accidental): The accidentals contained in this Chordrest."""
        return self._accidentals

    @property
    def ledgers(self):
        """set(LedgerLine): The ledger lines contained in this Chordrest.

        An empty set means no ledgers.
        """
        return self._ledgers

    @property
    def stem(self):
        """Stem or None: The Stem for the Chordrest."""
        return self._stem

    @property
    def flag(self):
        """Flag or None: The flag attached to the stem."""
        return self._flag

    @property
    def duration(self):
        """Beat: The length of this event.

        This is used to determine which (if any) `Flag`s, `RhythmDot`s,
        and `Notehead`/`Rest` styles. Higher level managers may also
        use this information to inform layout decisions and `Beam` groupings.
        """
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def ledger_line_positions(self):
        """set(int): A set of staff positions of needed ledger lines.

        Positions are in centered staff positions.

        An empty set means no ledger lines are needed.
        """
        highest = self.highest_notehead.staff_pos
        lowest = self.lowest_notehead.staff_pos
        # Join sets of needed ledgers above and below with union operator
        return (self.staff.ledgers_needed_for_y(lowest) |
                self.staff.ledgers_needed_for_y(highest))

    @property
    def rhythm_dot_positions(self):
        """iter(Point): The positions of all rhythm dots needed."""
        if self.rest:
            dot_start_x = self.rest.x + self.rest.bounding_rect.width
            dottables = {self.rest}
        else:
            dot_start_x = self.leftmost_notehead.x + self.notehead_column_width
            dottables = self.noteheads
        for i in range(self.duration.dot_count):
            for dottable in dottables:
                if dottable.y.value % 1 == 0:
                    # Dottable is on a line, add dot offset to space below
                    y_offset = self.staff.unit(-0.5)
                else:
                    y_offset = self.staff.unit(0)
                yield(Point(dot_start_x + (self.staff.unit(0.5) * i),
                            dottable.y + y_offset))
    @property
    def furthest_notehead(self):
        """Notehead or None: The `Notehead` furthest from the staff center"""
        return max(self.noteheads,
                   key=lambda n: abs(n.staff_pos - self.staff.center_pos_y),
                   default=None)

    @property
    def highest_notehead(self):
        """Notehead or None: The highest `Notehead` in the chord."""
        return min(self.noteheads,
                   key=lambda n: n.staff_pos,
                   default=None)

    @property
    def lowest_notehead(self):
        """Notehead or None: The lowest `Notehead` in the chord."""
        return max(self.noteheads,
                   key=lambda n: n.staff_pos,
                   default=None)

    @property
    def leftmost_notehead(self):
        """Notehead or None: the `Notehead` furthest to the left in the chord"""
        return min(self.noteheads,
                   key=lambda n: n.x,
                   default=None)

    @property
    def rightmost_notehead(self):
        """Notehead or None: the `Notehead` furthest to the right in the chord"""
        return max(self.noteheads,
                   key=lambda n: n.x,
                   default=None)

    @property
    def widest_notehead(self):
        """Notehead or None: the `Notehead` with the greatest `visual_width`"""
        return max(self.noteheads,
                   key=lambda n: n.visual_width,
                   default=None)

    @property
    def notehead_column_width(self):
        """Unit: The total width of all `Notehead`s in the chord"""
        if not self.noteheads:
            return self.staff.unit(0)
        else:
            left = self.leftmost_notehead.x
            extent = max((n.x + n.visual_width
                          for n in self.noteheads))
            return extent - left

    @property
    def noteheads_outside_staff(self):
        """set(Notehead): All noteheads which are above or below the staff"""
        return set(note for note in self.noteheads
                   if self.staff.y_outside_staff(note.staff_pos))

    @property
    def leftmost_notehead_outside_staff(self):
        """Notehead or None: the `Notehead` furthest to the left outside the staff"""
        return min(self.noteheads_outside_staff,
                   key=lambda n: n.x,
                   default=None)

    @property
    def rightmost_notehead_outside_staff(self):
        """Notehead or None: the `Notehead` furthest to the right outside the staff"""
        return max(self.noteheads_outside_staff,
                   key=lambda n: n.x,
                   default=None)

    @property
    def notehead_column_outside_staff_width(self):
        """Unit: The total width of any noteheads outside the staff"""
        if not self.noteheads:
            return self.staff.unit(0)
        else:
            left = self.leftmost_notehead_outside_staff.x
            extent = max((n.x + n.visual_width
                          for n in self.noteheads_outside_staff))
            return extent - left

    @property
    def stem_direction(self):
        """int: The direction of the stem, either `1` (down) or `-1` (up)

        Takes the notehead furthest from the center of the staff,
        and returns the opposite direction.

        If the furthest notehead is in the center of the staff,
        the direction defaults to `1`.

        This automatically calculated property may be overridden using
        its setter. To revert back to the automatically calculated value
        set this property to `None`.
        """
        if self._stem_direction_override is not None:
            return self._stem_direction_override
        furthest = self.furthest_notehead
        if furthest:
            return (1 if furthest.staff_pos <= self.staff.center_pos_y
                    else -1)
        else:
            return None

    @stem_direction.setter
    def stem_direction(self, value):
        self._stem_direction_override = value

    @property
    def stem_height(self):
        """Unit: The height of the stem"""
        flag_offset = Flag.vertical_offset_needed(self.duration,
                                                  self.staff.unit)
        min_abs_height = self.staff.unit(5) + flag_offset
        fitted_abs_height = (abs(self.lowest_notehead.y -
                                 self.highest_notehead.y) +
                             self.staff.unit(2) +
                             flag_offset)
        abs_height = max(min_abs_height, fitted_abs_height)
        return abs_height * self.stem_direction

    ######## PRIVATE METHODS ########

    def _render(self):
        if self.noteheads:
            # Chord-specific aux objects
            self._position_noteheads_horizontally()
            self._position_accidentals_horizontally()
            self._create_accidentals()
            self._create_ledgers()
            self._create_stem()
            self._create_flag()
        # Both rests and chords needs dots
        self._create_dots()
        super()._render()

    def _create_ledgers(self):
        """Create all required ledger lines and store them in `self.ledgers`

        Returns: None

        Warning: This should be called after _position_noteheads_horizontally()
                 as it relies on the position of noteheads in the chord to
                 calculate the position and length of the ledger lines
        """
        pos_x = self.leftmost_notehead.x
        length = self.notehead_column_outside_staff_width
        for staff_pos in self.ledger_line_positions:
            self.ledgers.add(LedgerLine(Point(pos_x, staff_pos), self, length))

    def _create_accidentals(self):
        padding = self.staff.unit(-1.2)
        for notehead in self.noteheads:
            if notehead.pitch.accidental_type is None:
                continue
            self.accidentals.add(Accidental((padding, self.staff.unit(0)),
                                            notehead.pitch.accidental_type,
                                            notehead))

    def _create_dots(self):
        """Create all the RhythmDots needed by this Chordrest."""
        for dot_pos in self.rhythm_dot_positions:
            self.dots.add(RhythmDot(dot_pos, self))

    def _create_stem(self):
        """Create a Stem and stores it in `self.stem`.

        Returns: None
        """
        self._stem = Stem(Point(self.staff.unit(0),
                                self.furthest_notehead.staff_pos),
                          self.stem_height, self)

    def _create_flag(self):
        """Create a Flag attached to self.stem and store it in self.flag

        Returns: None
        """
        if Flag.needs_flag(self.duration):
            self._flag = Flag(self.duration,
                              self.stem.direction,
                              self.stem.end_point)

    def _position_noteheads_horizontally(self):
        """Reposition noteheads so that they are laid out correctly

        Decides which noteheads lie on which side of the staff,
        and modifies positions when needed.

        Returns: None
        """
        # Find the preferred side of the stem for noteheads,
        # where 1 means right and -1 means left
        default_side = self.stem_direction
        # Start last staff pos at sentinel infinity position
        prev_staff_pos = self.staff.unit(float("inf"))
        # Start prev_side at wrong side so first note goes on the default side
        prev_side = -1 * default_side
        for note in sorted(self.noteheads,
                           key=lambda n: n.staff_pos,
                           reverse=(self.stem_direction == -1)):
            if abs(prev_staff_pos - note.staff_pos) < 1:
                # This note collides with previous, use switch sides
                prev_side = -1 * prev_side
            else:
                prev_side = default_side
            # Reposition, using prev_side (here) as the chosen side for this note
            if prev_side == -1:
                note.x -= note.visual_width
            # Lastly, update prev_staff_pos
            prev_staff_pos = note.staff_pos

    def _position_accidentals_horizontally(self):
        """Reposition accidentals so that they are laid out correctly

        TODO: Implement me

        Returns: None
        """
        pass
