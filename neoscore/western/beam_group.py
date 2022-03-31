from typing import NamedTuple, Optional, cast

from neoscore.core.brush import SimpleBrushDef
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.mapping import map_between, map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import SimplePenDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.models.directions import HorizontalDirection, VerticalDirection
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import ZERO, Unit
from neoscore.western.beam import Beam
from neoscore.western.chordrest import Chordrest


class BeamState(NamedTuple):
    """The state of a beam group at a note.

    (For convenience we describe these as applying to "notes" but they
    can apply to chords and beamed rests as well.)
    """

    flag_count: int
    break_depth: Optional[int] = None
    """Indicates a subgroup break after this note.

    This indicates the number of beams to cut a subdivision to after
    this beam position. The value must be less than `flag_count` and
    greater than 0.

    For example, `[BeamState(3), BeamState(3, break_depth=1),
    BeamState(3), BeamState(3)]` encodes four 32nd notes subdivided into
    2 groups of 2 connected by a single beam.
    
    Because the beam resolver is not meter-aware, it does not perform
    subdivision breaks unless explicitly requested with this field.
    """

    hook: Optional[HorizontalDirection] = None
    """Direction for beamlet hooks.

    If provided as an override, this only has an effect if the beam
    position requires a hook and that hook direction is
    ambiguous. This only applies in places where, within a beam
    subgroup, a position has more flags than its previous and
    following position, *and* those adjacent values are equal. For
    example, a sixteenth note surrounded by two eighth notes.
    """


def resolve_beams(specs: list[BeamState]) -> list[BeamState]:
    if len(specs) < 2:
        raise ValueError("Beam groups must have at least 2 members")
    states: list[BeamState] = []
    for i, (current_count, break_depth, current_hint_hook) in enumerate(specs):
        prev_count, prev_hint_break_depth, _ = (
            specs[i - 1] if i > 0 else (None, None, None)
        )
        next_count, next_hint_break_depth, _ = (
            specs[i + 1] if i < len(specs) - 1 else (None, None, None)
        )
        # Resolve hook
        hook = None
        if prev_count is None or (prev_hint_break_depth and next_count):
            # First item in group or subgroup
            next_count = cast(int, next_count)
            if current_count > next_count:
                hook = HorizontalDirection.RIGHT
        elif next_count is None:
            # Last item in group
            prev_count = cast(int, prev_count)
            if current_count > prev_count:
                hook = HorizontalDirection.LEFT
        else:
            # Item in middle of group
            if current_count > prev_count and current_count > next_count:
                if prev_count < next_count:
                    hook = HorizontalDirection.RIGHT
                elif prev_count > next_count:
                    hook = HorizontalDirection.LEFT
                else:
                    # Surrounding positions flag counts are equal, so
                    # hook direction is ambiguous. Allow override.
                    hook = current_hint_hook or HorizontalDirection.LEFT
        states.append(BeamState(current_count, break_depth, hook))
    return states


class BeamPathSpec(NamedTuple):
    """An intermediate representation of beam paths."""

    depth: int
    """The beam's 1-indexed vertical position in the beam stack.
    
    1 represents the outermost beam, 2 represents 1 inward, and so
    on. For example, in a beam stack connecting sixteenth notes,
    `depth=1` would represent the 8th note beam while `depth=2` would
    represent the 16th note beam. In this way, `depth` corresponds to
    the flag counts of represented durations.
    """

    start: int
    """Index of the starting position"""

    end: int | HorizontalDirection
    """Index of the ending position or a hook direction.

    If this is an index, it should be greater than `start`.
    """


def resolve_beam_layout(states: list[BeamState]) -> list[BeamPathSpec]:
    """Given a list of individual note beam states, work out how to render the beams."""
    # Iterate through beams from depth 0 to end, left to right.
    path_specs = []
    max_flag_count = max((state.flag_count for state in states))
    for depth in range(1, max_flag_count + 1):
        start_idx = None
        for i, state in enumerate(states):
            if start_idx is None:
                if state.flag_count >= depth:
                    start_idx = i
                else:
                    continue
            break_ends_beam = (
                state.break_depth is not None and state.break_depth < depth
            )
            next_depth_ends_beam = (
                i == len(states) - 1 or states[i + 1].flag_count < depth
            )
            if break_ends_beam or next_depth_ends_beam:
                # Beam ends after this state
                if start_idx == i:
                    # Beam only spanned one state, treat it as a hook
                    # Sanity check, hook should always be provided when required.
                    assert state.hook
                    path_specs.append(BeamPathSpec(depth, start_idx, state.hook))
                else:
                    path_specs.append(BeamPathSpec(depth, start_idx, i))
                start_idx = None
    return path_specs


class BeamGroupLine(NamedTuple):
    """Definition for the line along which a beam group's outermost beam runs."""

    start_y: Unit
    """The starting y position relative to the staff.

    When the starting x position is implied to be 0, this is line's y-intercept.
    """

    slope: float


# TODO HIGH test me


def resolve_beam_group_line(
    chordrests: list[Chordrest], direction: VerticalDirection
) -> BeamGroupLine:
    unit = chordrests[0].staff.unit
    first = chordrests[0]
    last = chordrests[-1]
    # Determine slope from first and last noteheads furthest on side opposite of beam
    if direction == VerticalDirection.DOWN:
        slope_start_ref_note = first.highest_notehead
        slope_end_ref_note = last.highest_notehead
    else:
        slope_start_ref_note = first.lowest_notehead
        slope_end_ref_note = last.lowest_notehead
    if slope_start_ref_note.y > slope_end_ref_note.y:
        delta_y = unit(-1)
    elif slope_start_ref_note.y == slope_end_ref_note.y:
        delta_y = ZERO
    else:
        delta_y = unit(1)
    delta_x = map_between(last, first).x
    slope = delta_y / delta_x
    # Now find the note closest to the beam's side
    if direction == VerticalDirection.DOWN:
        cr_with_closest_note = max(chordrests, key=lambda c: c.lowest_notehead.y)
        cr_x = map_between_x(first, cr_with_closest_note)
        closest_y = cr_with_closest_note.lowest_notehead.y
        nearest_beam_intersect = Point(cr_x, closest_y + unit(3.5))
    else:
        cr_with_closest_note = min(chordrests, key=lambda c: c.highest_notehead.y)
        cr_x = map_between_x(first, cr_with_closest_note)
        closest_y = cr_with_closest_note.highest_notehead.y
        nearest_beam_intersect = Point(cr_x, closest_y - unit(3.5))
    # Given a beam intersect and a slope, find the beam y at `start`
    # y = m(x - x1) + y1, where x = 0
    start_y = (slope * (-nearest_beam_intersect.x)) + nearest_beam_intersect.y
    return BeamGroupLine(start_y, slope)


def resolve_beam_direction(chordrests: list[Chordrest]) -> VerticalDirection:
    """Try to determine the best direction a beam group should go in.

    The algorithm works by determining the average y position of the
    outermost notes of each chord, then if that position lies above
    the middle staff line, placing the beam below (`DOWN`), and vice
    versa
    """
    middle_staff_pos = chordrests[0].staff.center_pos_y
    center = sum(
        [
            c.furthest_notehead.y if c.noteheads else middle_staff_pos
            for c in chordrests
        ],
        start=ZERO,
    ) / len(chordrests)
    if center > middle_staff_pos:
        return VerticalDirection.UP
    else:
        return VerticalDirection.DOWN


class BeamGroup(PositionedObject, HasMusicFont):
    def __init__(
        self,
        chordrests: list[Chordrest],
        font: Optional[MusicFont] = None,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
    ):
        """
        Args:
            chordrests: The notes or rests to beam across. This must have
                at least 2 items, all of which must be of durations requiring flags.
            font: A font override. If not provided, the beams are drawn with the font
                of the first chordrest given.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """
        if len(chordrests) < 2:
            raise ValueError("BeamGroup must have at least 2 Chordrests.")
        # Determine top beam path
        chordrests.sort(key=lambda c: c.x)
        self._chordrests = chordrests
        self._beams = []
        first = chordrests[0]
        last = chordrests[-1]
        super().__init__(ORIGIN, first)
        if font is None:
            font = HasMusicFont.find_music_font(self.parent)
        self._music_font = font
        beam_start_pos = ORIGIN
        # Work out beam direction, slope, and offset
        beam_direction = resolve_beam_direction(chordrests)
        beam_group_line = resolve_beam_group_line(chordrests, beam_direction)
        # Adjust stems to follow group line
        for c in chordrests:
            # y = m(x - x1) - y1, where x = 0
            c_relative_x = map_between_x(c, first)
            y = (beam_group_line.slope * c_relative_x) + beam_group_line.start_y
            c.stem.end_point.y = map_between(c.stem, self).y + y
            c.flag.remove()
            c._flag = None
        # Now create the beams!
        beam_thickness = self.music_font.engraving_defaults["beamThickness"]
        layer_step = (
            self.music_font.engraving_defaults["beamSpacing"] + beam_thickness
        ) * -first.stem.direction.value
        specs = BeamGroup._resolve_chordrest_beam_layout(chordrests)
        for spec in specs:
            start_parent = chordrests[spec.start].stem.end_point
            if isinstance(spec.end, int):
                end_parent = chordrests[spec.end].stem.end_point
                end_x = ZERO
            else:
                end_parent = start_parent
                end_x = beam_thickness * 2 * spec.end.value
            y = (spec.depth - 1) * layer_step
            self.beams.append(
                Beam((ZERO, y), start_parent, (end_x, y), end_parent, font, brush, pen)
            )

    @staticmethod
    def _resolve_chordrest_beam_layout(
        chordrests: list[Chordrest],
    ) -> list[BeamPathSpec]:
        states = resolve_beams(
            [
                BeamState(
                    c.duration.display.flag_count, c.beam_break_depth, c.beam_hook_dir
                )
                for c in chordrests
            ]
        )
        return resolve_beam_layout(states)

    @property
    def chordrests(self) -> list[Chordrest]:
        return self._chordrests

    @property
    def beams(self) -> list[Beam]:
        return self._beams

    @property
    def music_font(self) -> MusicFont:
        return self._music_font
