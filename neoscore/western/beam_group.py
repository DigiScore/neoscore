from dataclasses import dataclass
from typing import NamedTuple, Optional, cast

from neoscore.models.directions import HorizontalDirection

# wip sketching...


@dataclass
class BeamHint:
    break_depth: Optional[int] = None
    hook: Optional[HorizontalDirection] = None


@dataclass
class BeamState:
    flag_count: int
    break_depth: Optional[int] = None
    hook: Optional[HorizontalDirection] = None


# notice how BeamSpec is identical to BeamState...


class BeamSpec(NamedTuple):
    flag_count: int
    break_depth: Optional[int] = None
    """User-provided override setting break depths.

    This indicates the number of beams to cut a subdivision to after
    this beam position. The value must be less than `flag_count` and
    greater than 0.

    For example, `[BeamSpec(3), BeamSpec(3, break_depth=1),
    BeamSpec(3), BeamSpec(3)]` encodes four 32nd notes subdivided into
    2 groups of 2 connected by a single beam.
    
    Because the beam resolver is not meter-aware, it does not perform
    subdivision breaks unless explicitly requested with this field.

    """
    hook: Optional[HorizontalDirection] = None
    """User-provided override for hook direction.

    This only has an effect if the beam position requires a hook and
    that hook direction is ambiguous. This only applies in places
    where, within a beam subgroup, a position has more flags than its
    previous and following position, *and* those adjacent values are
    equal. For example, a sixteenth note surrounded by two eighth
    notes.
    """


def resolve_beams(specs: list[BeamSpec]) -> list[BeamState]:
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
            if state.break_depth is not None and state.break_depth < depth:
                break_ends_beam = True
            else:
                break_ends_beam = False
            if i == len(states) - 1 or states[i + 1].flag_count < depth:
                next_depth_ends_beam = True
            else:
                next_depth_ends_beam = False
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
