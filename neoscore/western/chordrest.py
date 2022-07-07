from typing import List, NamedTuple, Optional, Union

from backports.cached_property import cached_property

from neoscore.core.directions import DirectionX, DirectionY
from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit
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


class PitchAndGlyph(NamedTuple):
    """Used to define individual notes with one-off SMuFL glyphs."""

    pitch: PitchDef
    """The pitch for the notehead"""

    notehead_glyph: str
    """The SMuFL glyph name for the notehead"""


class Chordrest(PositionedObject, StaffObject):

    """A chord or a rest.

    This is a unified interface for conventionally notated
    musical notes/chords/rests. It can be given any number of pitches
    to be used as notes in the chord, or ``None`` for a rest.

    It will automatically generate and lay out:

    * :obj:`.Notehead`\ s if pitches are given
    * a :obj:`.Stem` if pitches are given and required by the given :obj:`.Duration`
    * a :obj:`.Flag` if pitches are given and required by the given ``Duration``
    * :obj:`.LedgerLine`\ s as needed (taking into consideration the given
      pitches and their location on the :obj:`.Staff`)
    * :obj:`.Accidental`\ s as needed by any given pitches
    * a :obj:`.Rest` if no pitches are given
    * :obj:`.RhythmDot`\ s if needed by the given ``Duration``

    Any accidentals given in pitches will be unconditionally drawn
    regardless of context and key signature.
    """

    # All cached properties which change on rebuilds *must* be registered here.
    _CACHED_PROPS = [
        "ledger_line_positions",
        "rhythm_dot_positions",
        "furthest_notehead",
        "highest_notehead",
        "lowest_notehead",
        "leftmost_notehead",
        "rightmost_notehead",
        "widest_notehead",
        "extra_attachment_point",
        "notehead_column_width",
        "noteheads_outside_staff",
        "leftmost_notehead_outside_staff",
        "rightmost_notehead_outside_staff",
        "notehead_column_outside_staff_width",
        "stem_height",
    ]

    def __init__(
        self,
        pos_x: Unit,
        staff: Staff,
        notes: Optional[List[Union[PitchDef, PitchAndGlyph]]],
        duration: DurationDef,
        rest_y: Optional[Unit] = None,
        stem_direction: Optional[DirectionY] = None,
        beam_break_depth: Optional[int] = None,
        beam_hook_dir: Optional[DirectionX] = None,
        table: NoteheadTable = notehead_tables.STANDARD,
    ):
        """
        Args:
            pos_x: The horizontal position in the staff
            staff: The staff the object is attached to
            notes: A list of pitches and optional notehead-specific data. If ``None``
                this indicates a rest. For simple notes and chords, this can typically
                be a list of pitch string shorthands (see :obj:`.Pitch.from_str`). Pitches
                with extended accidentals can be given by passing fully constructed
                ``Pitch`` objects. Individual notehead glyphs (by default taken from the
                given ``table``) can be overridden by passing a tuple of a pitch
                and a SMuFL glyph name string.
            duration: The written duration for the object.
            rest_y: The vertical position used by rests. This defaults to the center
                of the staff.
            stem_direction: An optional stem direction override. If omitted, the
                direction is automatically calculated to point away from
                the furthest-out notehead.
            beam_break_depth: Break depth used if in a :obj:`.BeamGroup`.
            beam_hook_dir: Beamlet hook direction used in a ``BeamGroup``.
            table: The set of noteheads to use according to ``duration``.
        """
        StaffObject.__init__(self, staff)
        PositionedObject.__init__(self, Point(pos_x, ZERO), staff)
        self.duration = duration
        self._noteheads = []
        self._accidentals = []
        self._ledgers = []
        self._dots = []
        self._notes = [] if notes is None else notes
        self._stem = None
        self._flag = None
        self._rest_y = rest_y
        self._rest = None
        self._stem_direction_override = stem_direction
        self._beam_break_depth = beam_break_depth
        self._beam_hook_dir = beam_hook_dir
        self._table = table
        self._rebuild()

    @property
    def notes(self) -> List[Union[PitchDef, PitchAndGlyph]]:
        return self._notes

    @notes.setter
    def notes(self, value: Optional[List[Union[PitchDef, PitchAndGlyph]]]):
        self._notes = [] if value is None else value
        self._rebuild()

    @property
    def noteheads(self) -> List[Notehead]:
        """The noteheads contained in this Chordrest."""
        return self._noteheads

    @property
    def rest_y(self) -> Optional[Unit]:
        """The vertical position used by generated rests.

        Defaults to the staff center.
        """
        return self._rest_y

    @rest_y.setter
    def rest_y(self, value: Optional[Unit]):
        self._rest_y = value
        self._rebuild()

    @property
    def rest(self) -> Optional[Rest]:
        """A rest glyph, if no noteheads exist."""
        return self._rest

    @property
    def accidentals(self) -> List[Accidental]:
        """The accidentals contained in this Chordrest."""
        return self._accidentals

    @property
    def ledgers(self) -> List[LedgerLine]:
        """The ledger lines contained in this Chordrest.

        An empty list means none are needed.
        """
        return self._ledgers

    @property
    def dots(self) -> List[RhythmDot]:
        return self._dots

    @property
    def stem(self) -> Optional[Stem]:
        """The stem for the Chordrest."""
        return self._stem

    @property
    def flag(self) -> Optional[Flag]:
        """The flag attached to the stem."""
        return self._flag

    @property
    def beam_break_depth(self) -> Optional[int]:
        """Break depth used if in a :obj:`.BeamGroup`.

        If this Chordrest is within a beam group, this triggers a beam subdivision break
        at this point. The value indicates the number of beams to which the subdivision
        breaks. For example, in run of 16th notes a ``beam_break_depth`` of ``1`` would
        indicate a subdivision break to 1 beam at this point.
        """
        return self._beam_break_depth

    @property
    def beam_hook_dir(self) -> Optional[DirectionX]:
        """Beamlet hook direction used in a :obj:`.BeamGroup`.

        If this Chordrest is within a beam group and this position is one requiring a
        beamlet hook whose direction is ambiguous, this controls that direction.
        """
        return self._beam_hook_dir

    @property
    def table(self) -> NoteheadTable:
        return self._table

    @table.setter
    def table(self, table: NoteheadTable):
        self._table = table
        self._rebuild()

    @property
    def duration(self) -> Duration:
        """The written length of this event.

        This affects many components of the chordrest.
        """
        return self._duration

    @duration.setter
    def duration(self, value: DurationDef):
        rebuild_needed = hasattr(self, "_duration")
        value = Duration.from_def(value)
        if value.display is None:
            raise ValueError(f"{value} cannot be represented as a single note")
        self._duration = value
        if rebuild_needed:
            self._rebuild()

    @cached_property
    def ledger_line_positions(self) -> List[Unit]:
        """A set of staff positions of needed ledger lines.

        Positions are in centered staff positions.

        An empty list means no ledger lines are needed.
        """
        highest = self.highest_notehead.y
        lowest = self.lowest_notehead.y
        # This could be optimized by only doing both ledger lookups if
        # ``highest`` and ``lowest`` are on opposite sides of the staff,
        # in which case the check-then-append step can be done
        # unconditionally.
        ledgers = self.staff.ledgers_needed_for_y(lowest)
        for ledger_pos in self.staff.ledgers_needed_for_y(highest):
            if ledger_pos not in ledgers:
                ledgers.append(ledger_pos)
        return ledgers

    @cached_property
    def rhythm_dot_positions(self) -> List[Point]:
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
        result = []
        for i in range(self.duration.display.dot_count):
            for dottable in dottables:
                if dottable.y.display_value % 1 == 0:
                    # Dottable is on a line, add dot offset to space below
                    y_offset = self.staff.unit(-0.5)
                else:
                    y_offset = self.staff.unit(0)
                result.append(
                    Point(
                        dot_start_x + (self.staff.unit(0.5) * i), dottable.y + y_offset
                    )
                )
        return result

    @cached_property
    def furthest_notehead(self) -> Optional[Notehead]:
        """The notehead furthest from the staff center"""
        return max(
            self.noteheads,
            key=lambda n: abs(n.y - self.staff.center_y),
            default=None,
        )

    @cached_property
    def highest_notehead(self) -> Optional[Notehead]:
        """The highest notehead in the chord."""
        return min(self.noteheads, key=lambda n: n.y, default=None)

    @cached_property
    def lowest_notehead(self) -> Optional[Notehead]:
        """The lowest notehead in the chord."""
        return max(self.noteheads, key=lambda n: n.y, default=None)

    @cached_property
    def leftmost_notehead(self) -> Optional[Notehead]:
        """The notehead furthest to the left in the chord"""
        return min(self.noteheads, key=lambda n: n.x, default=None)

    @cached_property
    def rightmost_notehead(self) -> Optional[Notehead]:
        """The notehead furthest to the right in the chord"""
        return max(self.noteheads, key=lambda n: n.x, default=None)

    @cached_property
    def extra_attachment_point(self) -> Point:
        """A point where common attachments like ornaments could go.

        For chords, this is a point centered above or below the outermost notehead
        opposite of the stem direction.

        For rests, this is a point centered above the rest.

        The returned point is relative to the Chordrest.
        """
        if self.rest:
            bounding_rect = self.rest.bounding_rect
            x = self.rest.x + bounding_rect.x + (bounding_rect.width / 2)
            y = self.rest.y + bounding_rect.y - self.staff.unit(1)
            return Point(x, y)
        if self.stem_direction == DirectionY.UP:
            notehead = self.lowest_notehead
            bounding_rect = notehead.bounding_rect
            y = notehead.y + bounding_rect.y + bounding_rect.height + self.staff.unit(1)
        else:
            notehead = self.highest_notehead
            bounding_rect = notehead.bounding_rect
            y = notehead.y + bounding_rect.y - self.staff.unit(1)
        x = notehead.x + bounding_rect.x + (bounding_rect.width / 2)
        return Point(x, y)

    @cached_property
    def notehead_column_width(self) -> Unit:
        """The width of the notehead column after layout"""
        leftmost_notehead = self.leftmost_notehead
        if not leftmost_notehead:
            return self.staff.unit(0)
        else:
            extent = max((n.x + n.visual_width for n in self.noteheads))
            return extent - leftmost_notehead.x

    @cached_property
    def noteheads_outside_staff(self) -> List[Notehead]:
        """All noteheads which are above or below the staff"""
        return [
            note
            for note in self.noteheads
            # Since ``note.parent == self`` and ``self.y == 0``
            if not self.staff.y_inside_staff(note.y)
        ]

    @cached_property
    def leftmost_notehead_outside_staff(self) -> Optional[Notehead]:
        """The notehead furthest to the left outside the staff"""
        return min(self.noteheads_outside_staff, key=lambda n: n.x, default=None)

    @cached_property
    def rightmost_notehead_outside_staff(self) -> Optional[Notehead]:
        """The notehead furthest to the right outside the staff"""
        return max(self.noteheads_outside_staff, key=lambda n: n.x, default=None)

    @cached_property
    def notehead_column_outside_staff_width(self) -> Unit:
        """The total width of any noteheads outside the staff"""
        left_bounding_note = self.leftmost_notehead_outside_staff
        if not left_bounding_note:
            return ZERO
        else:
            extent = max((n.x + n.visual_width for n in self.noteheads_outside_staff))
            return extent - left_bounding_note.x

    # Can't use cached_property here because a setter is needed. Could get around this
    # by storing this computation in an attr like self._stem_direction though.
    @property
    def stem_direction(self) -> DirectionY:
        """The direction of the stem

        Takes the notehead furthest from the center of the staff, and returns the
        opposite direction.

        If the furthest notehead is in the center of the staff, the direction defaults
        to ``DirectionY.DOWN``, unless the staff has only one line, in which case it
        defaults to ``DirectionY.UP`` as a convenience for percussion staves.

        This automatically calculated property may be overridden using its setter. To
        revert to the automatically calculated value set this property to ``None``.

        If there are no noteheads (meaning this Chordrest is a rest), this arbitrarily
        returns ``DirectionY.UP``.

        """
        if self._stem_direction_override:
            return self._stem_direction_override
        furthest = self.furthest_notehead
        if furthest is None:
            return DirectionY.UP
        if furthest.y < self.staff.center_y:
            return DirectionY.DOWN
        elif furthest.y == self.staff.center_y:
            if self.staff.line_count == 1:
                return DirectionY.UP
            else:
                return DirectionY.DOWN
        else:
            return DirectionY.UP

    @stem_direction.setter
    def stem_direction(self, value: Optional[DirectionY]):
        self._stem_direction_override = value
        self._rebuild()

    @cached_property
    def stem_height(self) -> Unit:
        """The height of the stem"""
        flag_offset = self.staff.unit(Flag.vertical_offset_needed(self.duration))
        min_abs_height = self.staff.unit(2.5) + flag_offset
        fitted_abs_height = (
            abs(self.lowest_notehead.y - self.highest_notehead.y)
            + self.staff.unit(2.5)
            + flag_offset
        )
        abs_height = max(min_abs_height, fitted_abs_height)
        return abs_height

    def _clear(self):
        for notehead in self.noteheads:
            notehead.remove()
        self._noteheads = []
        for accidental in self.accidentals:
            accidental.remove()
        self._accidentals = []
        for ledger in self.ledgers:
            ledger.remove()
        self._ledgers = []
        for dot in self.dots:
            dot.remove()
        self._dots = []
        if self.stem:
            self.stem.remove()
        self._stem = None
        if self.flag:
            self.flag.remove()
        self._flag = None
        if self.rest:
            self.rest.remove()
        self._rest = None
        for prop in Chordrest._CACHED_PROPS:
            self.__dict__.pop(prop, None)

    def _rebuild(self):
        """Generate or regenerate all child objects"""
        if self.noteheads or self.rest:
            # Clear existing glyphs
            self._clear()
        if self.notes:
            for note in self.notes:
                if isinstance(note, tuple) and len(note) == 2:
                    pitch = note[0]
                    glyph_override = note[1]
                else:
                    pitch = note
                    glyph_override = None
                self._noteheads.append(
                    Notehead(
                        ZERO,
                        self,
                        pitch,
                        self.duration,
                        table=self.table,
                        glyph_override=glyph_override,
                    )
                )
            self._rest = None
            self._create_stem()
            if self.stem:
                self._position_noteheads_around_stem()
            self._create_accidentals()
            self._position_accidentals_horizontally()
            self._create_ledgers()
            self._create_flag()
        else:
            rest_y = self.rest_y or self.staff.center_y
            self._rest = Rest(Point(self.staff.unit(0), rest_y), self, self.duration)
        # Both rests and chords needs dots
        self._create_dots()

    def _create_ledgers(self):
        """Create all required ledger lines and store them in ``self.ledgers``

        This should be called after _position_noteheads_horizontally()
        as it relies on the position of noteheads in the chord to
        calculate the position and length of the ledger lines
        """
        pos_x = self.leftmost_notehead.x
        length = self.notehead_column_outside_staff_width
        for staff_pos in self.ledger_line_positions:
            self.ledgers.append(LedgerLine(Point(pos_x, staff_pos), self, length))

    def _create_accidentals(self):
        for notehead in self.noteheads:
            if notehead.pitch.accidental is None:
                continue
            accidental = Accidental(
                # X value is a placeholder to be resolved
                # in _position_accidentals_horizontally
                (ZERO, notehead.y),
                self,
                notehead.pitch.accidental,
            )
            self.accidentals.append(accidental)

    def _create_dots(self):
        """Create all the RhythmDots needed by this Chordrest."""
        for dot_pos in self.rhythm_dot_positions:
            self.dots.append(RhythmDot(dot_pos, self))

    def _create_stem(self):
        """If needed, create a Stem and store it in ``self.stem``."""
        if not self.duration.display.requires_stem:
            return
        if self.stem_direction == DirectionY.UP:
            attached_notehead = self.lowest_notehead
            anchor_key = "stemUpSE"
        else:
            attached_notehead = self.highest_notehead
            anchor_key = "stemDownNW"
        resolved_anchor_y = ZERO
        # Special case guard needed for invisible noteheads without music chars
        if attached_notehead.text:
            anchors = attached_notehead.music_chars[0].glyph_info.anchors
            if anchors:
                resolved_anchor = anchors.get(anchor_key)
                if resolved_anchor:
                    resolved_anchor_y = resolved_anchor.y
        self._stem = Stem(
            Point(ZERO, attached_notehead.y + resolved_anchor_y),
            self,
            self.stem_direction,
            self.stem_height,
        )

    def _create_flag(self):
        """Create a Flag attached to ``self.stem`` and store it in ``self.flag``"""
        if self.duration.display.flag_count:
            self._flag = Flag(
                (self.stem.pen.thickness / -2, ZERO),
                self.stem.end_point,
                self.duration,
                self.stem.direction,
            )

    def _position_noteheads_around_stem(self):
        """Reposition noteheads so that they are laid out correctly around the stem.

        This should only be run if a stem exists.
        """
        # Find the preferred side of the stem for noteheads,
        default_side = (
            DirectionX.LEFT
            if self.stem_direction == DirectionY.UP
            else DirectionX.RIGHT
        )
        # Start last staff pos at sentinel infinity position.
        # Rather than working with staff positions, we can work with
        # ``Notehead.y`` values directly because we know they all share
        # ``self`` as a parent.
        prev_y = Unit(float("inf"))
        # Start prev_side at wrong side so first note goes on the default side
        prev_side = default_side.flip()
        for note in sorted(
            self.noteheads,
            key=lambda n: n.y,
            reverse=(self.stem_direction == DirectionY.UP),
        ):
            if abs(prev_y - note.y) < self.staff.unit(1):
                # This note collides with previous, switch sides
                prev_side = prev_side.flip()
            else:
                prev_side = default_side
            note.x = self._resolve_notehead_x_pos(note, prev_side)
            prev_y = note.y

    def _resolve_notehead_x_pos(
        self, notehead: Notehead, stem_side: DirectionX
    ) -> Unit:
        if not notehead.text:
            return ZERO
        anchors = notehead.music_chars[0].glyph_info.anchors
        if not anchors:
            if stem_side == DirectionX.LEFT:
                return -notehead.visual_width
            return ZERO
        stem_offset = self.stem.pen.thickness / 2
        if stem_side == DirectionX.LEFT:
            anchor_key = "stemUpSE"
            stem_offset *= -1
        else:
            anchor_key = "stemDownNW"
        return -(anchors[anchor_key].x + stem_offset)

    def _position_accidentals_horizontally(self):
        """Reposition accidentals so that they are laid out correctly

        This implementation is very basic and fails in some fairly common use-cases. A
        proper solution would likely involve totally redoing this. See
        https://github.com/DigiScore/neoscore/issues/32
        """
        # Rather than working with staff positions, we can work with
        # ``Accidental.y`` values directly because we know they all share
        # ``self`` as a parent.
        padding = self.staff.music_font.engraving_defaults["staffLineThickness"]
        notehead_col_edge_x = self.leftmost_notehead.x
        prev_side = None
        prev_acc = None
        prev_rect = None
        for acc in sorted(self.accidentals, key=lambda a: a.y):
            acc_rect = acc.bounding_rect
            shift_for_collision = False

            if (
                prev_acc
                and prev_side == DirectionX.RIGHT
                and (prev_acc.y + prev_rect.y + prev_rect.height > acc.y + acc_rect.y)
            ):
                # This accidental collides with previous, switch sides
                shift_for_collision = True
                prev_side = DirectionX.LEFT
            else:
                prev_side = DirectionX.RIGHT
            if shift_for_collision:
                acc.x = prev_acc.x - acc.bounding_rect.width
            else:
                acc.x = notehead_col_edge_x - acc.bounding_rect.width - padding
            prev_acc = acc
            prev_rect = acc_rect
