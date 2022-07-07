from typing import List, NamedTuple, Optional, Union, cast

from neoscore.core.brush import Brush, BrushDef
from neoscore.core.directions import DirectionX, DirectionY
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen, PenDef
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit
from neoscore.western.beam import Beam
from neoscore.western.chordrest import Chordrest


class _BeamState(NamedTuple):
    """The state of a beam group at a ``Chordrest`` position"""

    flag_count: int
    break_depth: Optional[int] = None
    """Indicates a subgroup break after this position.

    This indicates the number of beams to cut a subdivision to after this beam position.
    The value must be less than ``flag_count`` and greater than 0.

    For example, this encodes four 32nd notes subdivided into 2 groups of 2 connected by
    a single beam: ``[_BeamState(3), _BeamState(3, break_depth=1), _BeamState(3), _BeamState(3)]``

    Because the beam resolver is not meter-aware, it does not perform subdivision breaks
    unless explicitly requested with this field.
    """

    hook: Optional[DirectionX] = None
    """Direction for beamlet hooks.

    If provided as an override, this only has an effect if the beam
    position requires a hook and that hook direction is
    ambiguous. This only applies in places where, within a beam
    subgroup, a position has more flags than its previous and
    following position, *and* those adjacent values are equal. For
    example, a 16th note surrounded by two 8th notes.
    """


def _resolve_beam_hooks(specs: List[_BeamState]) -> List[_BeamState]:
    """Determine which states need hooks, accounting for overrides where sensible."""
    if len(specs) < 2:
        raise ValueError("Beam groups must have at least 2 members")
    states: List[_BeamState] = []
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
                hook = DirectionX.RIGHT
        elif next_count is None or (break_depth and break_depth < current_count):
            # Last item in group
            prev_count = cast(int, prev_count)
            if current_count > prev_count:
                hook = DirectionX.LEFT
        else:
            # Item in middle of group
            if current_count > prev_count and current_count > next_count:
                if prev_count < next_count:
                    hook = DirectionX.RIGHT
                elif prev_count > next_count:
                    hook = DirectionX.LEFT
                else:
                    # Surrounding positions flag counts are equal, so
                    # hook direction is ambiguous. Allow override.
                    hook = current_hint_hook or DirectionX.LEFT
        states.append(_BeamState(current_count, break_depth, hook))
    return states


class _BeamPathSpec(NamedTuple):
    """An intermediate representation of beam paths."""

    depth: int
    """The beam's 1-indexed vertical position in the beam stack.

    1 represents the outermost beam, 2 represents 1 inward, and so
    on. For example, in a beam stack connecting sixteenth notes,
    ``depth=1`` would represent the 8th note beam while ``depth=2`` would
    represent the 16th note beam. In this way, ``depth`` corresponds to
    the flag counts of represented durations.
    """

    start: int
    """Index of the starting position"""

    end: Union[int, DirectionX]
    """Index of the ending position or a hook direction.

    If this is an index, it should be greater than ``start``.
    """


def _resolve_beam_layout(states: List[_BeamState]) -> List[_BeamPathSpec]:
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
    """The line running along the outside of a group's outermost beam."""

    start_y: Unit
    """The starting y position relative to the staff.

    When the starting x position is implied to be 0, this is line's y-intercept.
    """

    slope: float


def _resolve_beam_group_line(
    chordrests: List[Chordrest], direction: DirectionY, font: MusicFont
) -> _BeamGroupLine:
    unit = chordrests[0].staff.unit
    first = chordrests[0]
    last = chordrests[-1]
    beam_group_height = _resolve_beam_group_height(chordrests, font)
    # Determine slope from the notes furthest on the side opposite of beam
    if direction == DirectionY.DOWN:
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
    delta_x = last.map_to(first).x
    slope = delta_y / delta_x
    # Now find the note closest to the beam's side
    if direction == DirectionY.DOWN:
        cr_with_closest_note = max(chordrests, key=lambda c: c.lowest_notehead.y)
        cr_x = first.map_x_to(cr_with_closest_note)
        closest_y = cr_with_closest_note.lowest_notehead.y
        nearest_beam_intersect = Point(cr_x, closest_y + unit(2.5) + beam_group_height)
    else:
        cr_with_closest_note = min(chordrests, key=lambda c: c.highest_notehead.y)
        cr_x = first.map_x_to(cr_with_closest_note)
        closest_y = cr_with_closest_note.highest_notehead.y
        nearest_beam_intersect = Point(cr_x, closest_y - unit(2.5) - beam_group_height)
    # Given a beam intersect and a slope, find the beam y at ``start``
    # y = m(x - x1) + y1, where x = 0
    start_y = (slope * (-nearest_beam_intersect.x)) + nearest_beam_intersect.y
    return _BeamGroupLine(start_y, slope)


def _beam_layer_height(font: MusicFont):
    """Determine the height of a beam and its vertical padding in a given font."""
    return (
        font.engraving_defaults["beamSpacing"]
        + font.engraving_defaults["beamThickness"]
    )


def _resolve_beam_group_height(chordrests: List[Chordrest], font: MusicFont) -> Unit:
    """Find the vertical height occupied by a beam group spanning the given Chordrests.

    This determines the maximum beam depth required and uses it to
    calculate the expected maximum height in the group.
    """
    max_depth = max((c.duration.display.flag_count for c in chordrests))
    return max_depth * _beam_layer_height(font)


def _resolve_beam_direction(chordrests: List[Chordrest]) -> DirectionY:
    """Try to determine the best direction a beam group should go in.

    The algorithm works by determining the average y position of the
    outermost notes of each chord, then if that position lies above
    the middle staff line, placing the beam below (``DOWN``), and vice
    versa
    """
    middle_staff_pos = chordrests[0].staff.center_y
    s = ZERO
    for c in chordrests:
        s += c.furthest_notehead.y if c.noteheads else middle_staff_pos
    avg = s / len(chordrests)
    if avg > middle_staff_pos:
        return DirectionY.UP
    else:
        return DirectionY.DOWN


class BeamGroup(PositionedObject, HasMusicFont):
    """A beam group spanning a collection of Chordrests.

    This analyzes the given chordrests to determine a reasonable beam layout. The
    beaming algorithm does not take into account metric subdivisions; instead it
    greedily tries to beam together as many notes as possible. Subdivisions can be
    specified by setting :obj:`.Chordrest.beam_break_depth`, which indicates a break
    after the chord to the given beam count.

    While in most situations, beamlet "hooks" (as in a dotted 8th note followed by a 16th
    note) unambiguously must point right or left, there are some cases where it is
    ambiguous. For example, a 16th note between two 8th notes could have its beamlet
    point left or right. In these situations, ``BeamGroup`` will point it left by
    default, but users can override this by setting :obj:`.Chordrest.beam_hook_dir`.

    The beam direction and slant angle are determined automatically based on the given
    notes. The direction can be overridden in ``BeamGroup``'s constructor.

    Beam layout automatically modifies spanned chordrests by snapping their stems to the
    beam line and, if this causes a stem flip, correcting the chordrest component
    layout.

    This currently has some limitations:

    * It does not support beamed rests
    * It does not respond well to mutations. If being used in interactive or animated
      situations, the group likely will need to be destroyed and recreated after any
      changes affecting its chordrests.
    """

    def __init__(
        self,
        chordrests: List[Chordrest],
        direction: Optional[DirectionY] = None,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            chordrests: The notes or rests to beam across. This must have
                at least 2 items, all of which must be of durations requiring flags.
            direction: Override for the beam direction. Otherwise, the beam direction
                is automatically chosen based on the given chordrests.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with. To ensure perfect overlaps with stems,
                this should have the same thickness of stems, derived from the
                ``MusicFont`` engraving default ``"stemThickness``.
        """
        if len(chordrests) < 2:
            raise ValueError("BeamGroup must have at least 2 Chordrests.")
        # Determine top beam path
        chordrests.sort(key=lambda c: c.x)
        self._chordrests = chordrests
        self._beams: List[Beam] = []
        super().__init__(ORIGIN, chordrests[0])
        if font is None:
            font = HasMusicFont.find_music_font(self.parent)
        self._music_font = font
        # Load engraving defaults
        self._beam_thickness = self.music_font.engraving_defaults["beamThickness"]
        self._stem_thickness = self.music_font.engraving_defaults["stemThickness"]
        # Use same pen as stem to ensure perfectly aligned overlap
        self._brush = Brush.from_def(brush) if brush else Brush()
        self._pen = Pen.from_def(pen) if pen else Pen(thickness=self._stem_thickness)
        self._direction = direction or _resolve_beam_direction(self._chordrests)
        self._create_beams()

    def _create_beams(self):
        # Work out beam direction, slope, and offset
        beam_group_line = _resolve_beam_group_line(
            self._chordrests, self.direction, self.music_font
        )
        # Adjust stems to follow group line
        for c in self._chordrests:
            # y = m(x - x1) - y1, where x = 0
            c_relative_x = c.map_x_to(self._chordrests[0])
            y = (beam_group_line.slope * c_relative_x) + beam_group_line.start_y
            # (This direction checking approach will not work for kneed beams)
            if self.direction != c.stem.direction:
                c.stem_direction = self.direction
            adjusted_stem_end_y = c.stem.map_to(self).y + y
            c.stem.end_point.y = adjusted_stem_end_y
            c.flag.remove()
            c._flag = None
        # Now create the beams!
        layer_step = _beam_layer_height(self.music_font) * -self.direction.value
        specs = BeamGroup._resolve_chordrest_beam_layout(self._chordrests)
        base_y = -self._beam_thickness if self.direction == DirectionY.DOWN else ZERO
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
        chordrests: List[Chordrest],
    ) -> List[_BeamPathSpec]:
        states = _resolve_beam_hooks(
            [
                _BeamState(
                    c.duration.display.flag_count, c.beam_break_depth, c.beam_hook_dir
                )
                for c in chordrests
            ]
        )
        return _resolve_beam_layout(states)

    @property
    def direction(self) -> DirectionY:
        return self._direction

    @property
    def chordrests(self) -> List[Chordrest]:
        return self._chordrests

    @property
    def beams(self) -> List[Beam]:
        return self._beams

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    def remove(self):
        # Since the beams are actually not children of the beam group
        # (which is not ideal), we need to ensure they are removed
        # when the group is.
        for beam in self.beams:
            beam.remove()
        super().remove()
