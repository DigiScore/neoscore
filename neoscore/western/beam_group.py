from typing import NamedTuple, Optional, cast

from neoscore.core.brush import Brush, BrushDef
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.mapping import map_between, map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen, PenDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.models.directions import HorizontalDirection, VerticalDirection
from neoscore.utils.math_helpers import sign
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import ZERO, Unit
from neoscore.western.beam import Beam
from neoscore.western.chordrest import Chordrest


class _BeamState(NamedTuple):
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

    For example, `[_BeamState(3), _BeamState(3, break_depth=1),
    _BeamState(3), _BeamState(3)]` encodes four 32nd notes subdivided into
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


def _resolve_beam_states(specs: list[_BeamState]) -> list[_BeamState]:
    if len(specs) < 2:
        raise ValueError("Beam groups must have at least 2 members")
    states: list[_BeamState] = []
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
        states.append(_BeamState(current_count, break_depth, hook))
    return states


class _BeamPathSpec(NamedTuple):
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


def _resolve_beam_layout(states: list[_BeamState]) -> list[_BeamPathSpec]:
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
                    path_specs.append(_BeamPathSpec(depth, start_idx, state.hook))
                else:
                    path_specs.append(_BeamPathSpec(depth, start_idx, i))
                start_idx = None
    return path_specs


class _BeamGroupLine(NamedTuple):
    """Definition for the line along which a beam group's outermost beam runs."""

    start_y: Unit
    """The starting y position relative to the staff.

    When the starting x position is implied to be 0, this is line's y-intercept.
    """

    slope: float


def _resolve_beam_group_line(
    chordrests: list[Chordrest], direction: VerticalDirection, font: MusicFont
) -> _BeamGroupLine:
    unit = chordrests[0].staff.unit
    first = chordrests[0]
    last = chordrests[-1]
    beam_thickness = font.engraving_defaults["beamThickness"]
    beam_group_height = _resolve_beam_group_height(chordrests, font)
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
        nearest_beam_intersect = Point(cr_x, closest_y + unit(2.5) + beam_group_height)
    else:
        cr_with_closest_note = min(chordrests, key=lambda c: c.highest_notehead.y)
        cr_x = map_between_x(first, cr_with_closest_note)
        closest_y = cr_with_closest_note.highest_notehead.y
        nearest_beam_intersect = Point(cr_x, closest_y - unit(2.5) - beam_group_height)
    # Given a beam intersect and a slope, find the beam y at `start`
    # y = m(x - x1) + y1, where x = 0
    start_y = (slope * (-nearest_beam_intersect.x)) + nearest_beam_intersect.y
    return _BeamGroupLine(start_y, slope)


def _beam_layer_height(font: MusicFont):
    """Determine the height of a beam and it's vertical padding in a given font."""
    return (
        font.engraving_defaults["beamSpacing"]
        + font.engraving_defaults["beamThickness"]
    )


def _resolve_beam_group_height(chordrests: list[Chordrest], font: MusicFont) -> Unit:
    """Find the vertical height occupied by a beam group spanning the given Chordrests.

    This determines the maximum beam depth required and uses it to
    calculate the expected maximum height in the group.
    """
    max_depth = max((c.duration.display.flag_count for c in chordrests))
    return max_depth * _beam_layer_height(font)


def _resolve_beam_direction(chordrests: list[Chordrest]) -> VerticalDirection:
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
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            chordrests: The notes or rests to beam across. This must have
                at least 2 items, all of which must be of durations requiring flags.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with. To ensure perfect overlaps with stems,
                this should have the same thickness of stems, derived from the
                `MusicFont` engraving default `"stemThickness`.
        """
        if len(chordrests) < 2:
            raise ValueError("BeamGroup must have at least 2 Chordrests.")
        # Determine top beam path
        chordrests.sort(key=lambda c: c.x)
        self._chordrests = chordrests
        self._beams = []
        super().__init__(ORIGIN, chordrests[0])
        if font is None:
            font = HasMusicFont.find_music_font(self.parent)
        self._music_font = font
        # Load engraving defaults
        self._beam_thickness = self.music_font.engraving_defaults["beamThickness"]
        self._stem_thickness = self.music_font.engraving_defaults["stemThickness"]
        # Use same pen as stem to ensure perfectly aligned overlap
        self._brush = Brush.from_def(brush)
        self._pen = Pen.from_def(pen) if pen else Pen(thickness=self._stem_thickness)
        self._create_beams()

    def _create_beams(self):
        # Work out beam direction, slope, and offset
        beam_direction = _resolve_beam_direction(self._chordrests)
        beam_group_line = _resolve_beam_group_line(
            self._chordrests, beam_direction, self.music_font
        )
        # Adjust stems to follow group line
        for c in self._chordrests:
            # y = m(x - x1) - y1, where x = 0
            c_relative_x = map_between_x(c, self._chordrests[0])
            y = (beam_group_line.slope * c_relative_x) + beam_group_line.start_y
            original_stem_sign = sign(c.stem.end_point.y)
            adjusted_stem_end_y = map_between(c.stem, self).y + y
            if sign(adjusted_stem_end_y) != original_stem_sign:
                # Need to re-layout chord notes because stem flipped
                # Very inefficiently rebuild the whole chordrest for this
                c.stem_direction = VerticalDirection.from_sign(adjusted_stem_end_y)
                c.rebuild()
            c.stem.end_point.y = adjusted_stem_end_y
            c.flag.remove()
            c._flag = None
        # Now create the beams!
        layer_step = _beam_layer_height(self.music_font) * -beam_direction.value
        specs = BeamGroup._resolve_chordrest_beam_layout(self._chordrests)
        base_y = (
            -self._beam_thickness if beam_direction == VerticalDirection.DOWN else ZERO
        )
        for spec in specs:
            start_parent = self._chordrests[spec.start].stem.end_point
            start_y = base_y + ((spec.depth - 1) * layer_step)
            if isinstance(spec.end, int):
                end_parent = self._chordrests[spec.end].stem.end_point
                end_x = ZERO
                end_y = start_y
            else:
                end_parent = start_parent
                end_x = self._beam_thickness * 2 * spec.end.value
                end_y = start_y + (-end_x * beam_group_line.slope)
            self.beams.append(
                Beam(
                    (ZERO, start_y),
                    start_parent,
                    (end_x, end_y),
                    end_parent,
                    self.music_font,
                    self._brush,
                    self._pen,
                )
            )

    @staticmethod
    def _resolve_chordrest_beam_layout(
        chordrests: list[Chordrest],
    ) -> list[_BeamPathSpec]:
        states = _resolve_beam_states(
            [
                _BeamState(
                    c.duration.display.flag_count, c.beam_break_depth, c.beam_hook_dir
                )
                for c in chordrests
            ]
        )
        return _resolve_beam_layout(states)

    @property
    def chordrests(self) -> list[Chordrest]:
        return self._chordrests

    @property
    def beams(self) -> list[Beam]:
        return self._beams

    @property
    def music_font(self) -> MusicFont:
        return self._music_font
