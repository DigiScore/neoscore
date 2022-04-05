from collections.abc import Iterable
from typing import Optional

from neoscore.core.directions import HorizontalDirection, VerticalDirection
from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import ZERO, Unit
from neoscore.western import notehead_tables
from neoscore.western.accidental import Accidental
from neoscore.western.duration import Duration, DurationDef
from neoscore.western.flag import Flag
from neoscore.western.ledger_line import LedgerLine
from neoscore.western.notehead import Notehead
from neoscore.western.notehead_tables import NoteheadTable
from neoscore.western.pitch import PitchDef
from neoscore.western.rest import Rest
from neoscore.western.rhythm_dot import RhythmDot
from neoscore.western.staff import Staff
from neoscore.western.staff_object import StaffObject
from neoscore.western.stem import Stem

# TODO MEDIUM this is not responsive to post-init modification.

# TODO MEDIUM align noteheads and stems properly using glyph anchor metadata
# see https://w3c.github.io/smufl/latest/specification/glyph-registration-notes-flags.html
# do this once #2 (glyph info refactor) is finished


class Chordrest(PositionedObject, StaffObject):

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

    The given pitches are treated mostly as written pitches. The only
    transposition automatically applied to them is octave
    transpositions from `OctaveLine`s.

    Any accidentals given in pitches will be unconditionally drawn
    regardless of context and key signature.
    """

    def __init__(
        self,
        pos_x: Unit,
        staff: Staff,
        pitches: Optional[list[PitchDef]],
        duration: DurationDef,
        stem_direction: Optional[VerticalDirection] = None,
        beam_break_depth: Optional[int] = None,
        beam_hook_dir: Optional[HorizontalDirection] = None,
        notehead_table: NoteheadTable = notehead_tables.STANDARD,
    ):
        """
        Args:
            pos_x: The horizontal position
            staff: The staff the object is attached to
            pitches: A list of pitch strings representing noteheads.
                An empty list or `None` indicates a rest.
            duration: The duration of the Chordrest
            stem_direction: An optional stem direction override
                where `1` points down and `-1` points up. If omitted, the
                direction is automatically calculated to point away from
                the furthest-out notehead.
            beam_break_depth: Break depth used if in a `BeamGroup`.
            beam_hook_dir: Beamlet hook direction used in a `BeamGroup`.
            notehead_table: The set of noteheads to use according to `duration`.
        """
        StaffObject.__init__(self, staff)
        PositionedObject.__init__(self, Point(pos_x, ZERO), staff)
        self.duration = duration
        self._noteheads = set()
        self._accidentals = set()
        self._ledgers = set()
        self._dots = set()
        self._pitches = pitches
        self._stem = None
        self._flag = None
        self._rest = None
        self._stem_direction_override = stem_direction
        self._beam_break_depth = beam_break_depth
        self._beam_hook_dir = beam_hook_dir
        self._notehead_table = notehead_table
        self.rebuild()

    ######## PUBLIC PROPERTIES ########

    @property
    def pitches(self) -> Optional[list[PitchDef]]:
        return self._pitches

    @pitches.setter
    def pitches(self, value: Optional[list[PitchDef]]):
        self._pitches = value

    @property
    def noteheads(self) -> set[Notehead]:
        """The noteheads contained in this Chordrest."""
        return self._noteheads

    @property
    def rest(self) -> Optional[Rest]:
        """A Rest glyph, if no noteheads exist."""
        return self._rest

    @rest.setter
    def rest(self, value: Optional[Rest]):
        self._rest = value

    @property
    def accidentals(self) -> set[Accidental]:
        """The accidentals contained in this Chordrest."""
        return self._accidentals

    @property
    def ledgers(self) -> set[LedgerLine]:
        """The ledger lines contained in this Chordrest.

        An empty set means no ledgers.
        """
        return self._ledgers

    @property
    def dots(self) -> set[RhythmDot]:
        return self._dots

    @property
    def stem(self) -> Optional[Stem]:
        """The Stem for the Chordrest."""
        return self._stem

    @property
    def flag(self) -> Optional[Flag]:
        """The flag attached to the stem."""
        return self._flag

    @property
    def beam_break_depth(self) -> Optional[int]:
        """Break depth used if in a `BeamGroup`.

        If this Chordrest is within a beam group, this triggers a
        beam subdivision break at this point. The value indicates the
        number of beams to which the subdivision breaks. For example,
        in run of 16th notes a `beam_break_depth` of `1` would
        indicate a subdivision break to 1 beam at this point.
        """
        return self._beam_break_depth

    @property
    def beam_hook_dir(self) -> Optional[HorizontalDirection]:
        """Beamlet hook direction used in a `BeamGroup`.

        If this Chordrest is within a beam group and this position is
        one requiring a beamlet hook whose direction is ambiguous,
        this controls that direction.
        """
        return self._beam_hook_dir

    @property
    def notehead_table(self) -> NoteheadTable:
        return self._notehead_table

    @notehead_table.setter
    def notehead_table(self, table: NoteheadTable):
        self._notehead_table = table

    @property
    def duration(self) -> Duration:
        """The length of this event.

        This is used to determine which (if any) `Flag`s, `RhythmDot`s,
        and `Notehead`/`Rest` styles. Higher level managers may also
        use this information to inform layout decisions and `Beam` groupings.
        """
        return self._duration

    @duration.setter
    def duration(self, value: DurationDef):
        value = Duration.from_def(value)
        if value.display is None:
            raise ValueError(f"{value} cannot be represented as a single note")
        self._duration = value

    @property
    def ledger_line_positions(self) -> list[Unit]:
        """A set of staff positions of needed ledger lines.

        Positions are in centered staff positions.

        An empty set means no ledger lines are needed.
        """
        highest = self.highest_notehead.y
        lowest = self.lowest_notehead.y
        # This could be optimized by only doing both ledger lookups if
        # `highest` and `lowest` are on opposite sides of the staff,
        # in which case the check-then-append step can be done
        # unconditionally.
        ledgers = self.staff.ledgers_needed_for_y(lowest)
        for ledger_pos in self.staff.ledgers_needed_for_y(highest):
            if ledger_pos not in ledgers:
                ledgers.append(ledger_pos)
        return ledgers

    @property
    def rhythm_dot_positions(self) -> Iterable[Point]:
        """The positions of all rhythm dots needed."""
        start_padding = self.staff.unit(0.25)
        if self.rest:
            dot_start_x = self.rest.x + self.rest.bounding_rect.width + start_padding
            dottables = {self.rest}
        else:
            dot_start_x = (
                self.leftmost_notehead.x + self.notehead_column_width + start_padding
            )
            dottables = self.noteheads
        for i in range(self.duration.display.dot_count):
            for dottable in dottables:
                if dottable.y.display_value % 1 == 0:
                    # Dottable is on a line, add dot offset to space below
                    y_offset = self.staff.unit(-0.5)
                else:
                    y_offset = self.staff.unit(0)
                yield (
                    Point(
                        dot_start_x + (self.staff.unit(0.5) * i), dottable.y + y_offset
                    )
                )

    @property
    def furthest_notehead(self) -> Optional[Notehead]:
        """The `Notehead` furthest from the staff center"""
        return max(
            self.noteheads,
            key=lambda n: abs(n.y - self.staff.center_y),
            default=None,
        )

    @property
    def highest_notehead(self) -> Optional[Notehead]:
        """The highest `Notehead` in the chord."""
        return min(self.noteheads, key=lambda n: n.y, default=None)

    @property
    def lowest_notehead(self) -> Optional[Notehead]:
        """The lowest `Notehead` in the chord."""
        return max(self.noteheads, key=lambda n: n.y, default=None)

    @property
    def leftmost_notehead(self) -> Optional[Notehead]:
        """The `Notehead` furthest to the left in the chord"""
        return min(self.noteheads, key=lambda n: n.x, default=None)

    @property
    def rightmost_notehead(self) -> Optional[Notehead]:
        """The `Notehead` furthest to the right in the chord"""
        return max(self.noteheads, key=lambda n: n.x, default=None)

    @property
    def widest_notehead(self) -> Optional[Notehead]:
        """The `Notehead` with the greatest `visual_width`"""
        return max(self.noteheads, key=lambda n: n.visual_width, default=None)

    @property
    def notehead_column_width(self) -> Unit:
        """The total width of all `Notehead`s in the chord"""
        leftmost_notehead = self.leftmost_notehead
        if not leftmost_notehead:
            return self.staff.unit(0)
        else:
            extent = max((n.x + n.visual_width for n in self.noteheads))
            return extent - leftmost_notehead.x

    @property
    def noteheads_outside_staff(self) -> Iterable[Notehead]:
        """All noteheads which are above or below the staff"""
        return (
            note
            for note in self.noteheads
            # Since `note.parent == self` and `self.y == 0`
            if not self.staff.y_inside_staff(note.y)
        )

    @property
    def leftmost_notehead_outside_staff(self) -> Optional[Notehead]:
        """The `Notehead` furthest to the left outside the staff"""
        return min(self.noteheads_outside_staff, key=lambda n: n.x, default=None)

    @property
    def rightmost_notehead_outside_staff(self) -> Optional[Notehead]:
        """The `Notehead` furthest to the right outside the staff"""
        return max(self.noteheads_outside_staff, key=lambda n: n.x, default=None)

    @property
    def notehead_column_outside_staff_width(self) -> Unit:
        """The total width of any noteheads outside the staff"""
        left_bounding_note = self.leftmost_notehead_outside_staff
        if not left_bounding_note:
            return ZERO
        else:
            extent = max((n.x + n.visual_width for n in self.noteheads_outside_staff))
            return extent - left_bounding_note.x

    @property
    def stem_direction(self) -> VerticalDirection:
        """The direction of the stem

        Takes the notehead furthest from the center of the staff,
        and returns the opposite direction.

        If the furthest notehead is in the center of the staff, the
        direction defaults to `VerticalDirection.DOWN`, unless the
        staff has only one line, in which case it defaults to
        `VerticalDirection.UP` as a convenience for percussion staves.

        This automatically calculated property may be overridden using
        its setter. To revert back to the automatically calculated value
        set this property to `None`.

        If there are no noteheads (meaning this Chordrest is a rest),
        this arbitrarily returns `VerticalDirection.UP`.

        """
        if self._stem_direction_override:
            return self._stem_direction_override
        furthest = self.furthest_notehead
        if furthest is None:
            return VerticalDirection.UP
        if furthest.y < self.staff.center_y:
            return VerticalDirection.DOWN
        elif furthest.y == self.staff.center_y:
            if self.staff.line_count == 1:
                return VerticalDirection.UP
            else:
                return VerticalDirection.DOWN
        else:
            return VerticalDirection.UP

    @stem_direction.setter
    def stem_direction(self, value: Optional[VerticalDirection]):
        self._stem_direction_override = value

    @property
    def stem_height(self) -> Unit:
        """The height of the stem"""
        flag_offset = self.staff.unit(Flag.vertical_offset_needed(self.duration))
        min_abs_height = self.staff.unit(3) + flag_offset
        fitted_abs_height = (
            abs(self.lowest_notehead.y - self.highest_notehead.y)
            + self.staff.unit(2)
            + flag_offset
        )
        abs_height = max(min_abs_height, fitted_abs_height)
        return abs_height * self.stem_direction.value

    ######## PRIVATE METHODS ########

    def _clear(self):
        for notehead in self.noteheads:
            notehead.remove()
        self._noteheads = set()
        for accidental in self.accidentals:
            accidental.remove()
        self._accidentals = set()
        for ledger in self.ledgers:
            ledger.remove()
        self._ledgers = set()
        for dot in self.dots:
            dot.remove()
        self._dots = set()
        if self.stem:
            self.stem.remove()
        self._stem = None
        if self.rest:
            self.rest.remove()
        self._rest = None

    def rebuild(self):
        """Generate or regenerate all child objects"""
        if self.noteheads or self.rest:
            # Clear existing glyphs
            self._clear()
        if self.pitches:
            for pitch in self.pitches:
                self._noteheads.add(
                    Notehead(
                        ZERO,
                        self,
                        pitch,
                        self.duration,
                        notehead_table=self.notehead_table,
                    )
                )
            self.rest = None
            self._position_noteheads_horizontally()
            self._position_accidentals_horizontally()
            self._create_accidentals()
            self._create_ledgers()
            self._create_stem()
            self._create_flag()
        else:
            # TODO LOW support explicit rest Y positioning
            self.rest = Rest(
                Point(self.staff.unit(0), self.staff.unit(2)), self, self.duration
            )
        # Both rests and chords needs dots
        self._create_dots()
        pass

    def _render(self):
        super()._render()

    def _create_ledgers(self):
        """Create all required ledger lines and store them in `self.ledgers`

        This should be called after _position_noteheads_horizontally()
        as it relies on the position of noteheads in the chord to
        calculate the position and length of the ledger lines
        """
        pos_x = self.leftmost_notehead.x
        length = self.notehead_column_outside_staff_width
        for staff_pos in self.ledger_line_positions:
            self.ledgers.add(LedgerLine(Point(pos_x, staff_pos), self, length))

    def _create_accidentals(self):
        padding = self.staff.music_font.engraving_defaults["staffLineThickness"]
        for notehead in self.noteheads:
            if notehead.pitch.accidental is None:
                continue
            accidental = Accidental(
                ORIGIN,
                notehead,
                notehead.pitch.accidental,
            )
            accidental.x -= accidental.bounding_rect.width + padding
            self.accidentals.add(accidental)

    def _create_dots(self):
        """Create all the RhythmDots needed by this Chordrest."""
        for dot_pos in self.rhythm_dot_positions:
            self.dots.add(RhythmDot(dot_pos, self))

    # TODO HIGH this y attachment point is wrong Should be the
    # furthest in the direction opposite of stem direction.
    # Fix after #4

    def _create_stem(self):
        """If needed, create a Stem and store it in `self.stem`."""
        if not self.duration.display.requires_stem:
            return
        self._stem = Stem(
            Point(self.staff.unit(0), self.furthest_notehead.y),
            self,
            self.stem_height,
        )

    def _create_flag(self):
        """Create a Flag attached to self.stem and store it in `self.flag`"""
        if self.duration.display.flag_count:
            self._flag = Flag(
                ORIGIN, self.stem.end_point, self.duration, self.stem.direction
            )

    def _position_noteheads_horizontally(self):
        """Reposition noteheads so that they are laid out correctly

        Decides which noteheads lie on which side of the stem,
        and modifies positions when needed.
        """
        # Find the preferred side of the stem for noteheads,
        # where 1 means right and -1 means left
        default_side = self.stem_direction.value
        # Start last staff pos at sentinel infinity position.
        # Rather than working with staff positions, we can work with
        # `Notehead.y` values directly because we know they all share
        # `self` as a parent.
        prev_y = Unit(float("inf"))
        # Start prev_side at wrong side so first note goes on the default side
        prev_side = -1 * default_side
        for note in sorted(
            self.noteheads,
            key=lambda n: n.y,
            reverse=(self.stem_direction == VerticalDirection.UP),
        ):
            if abs(prev_y - note.y) < self.staff.unit(1):
                # This note collides with previous, use switch sides
                prev_side = -1 * prev_side
            else:
                prev_side = default_side
            # Reposition, using prev_side (here) as the chosen side for this note
            if prev_side == -1:
                note.x -= note.visual_width
            # Lastly, update prev_y
            prev_y = note.y

    def _position_accidentals_horizontally(self):
        """Reposition accidentals so that they are laid out correctly

        TODO LOW: Implement me

        Returns: None
        """
        pass
