from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple, Optional, cast

# wip sketching...


class BeamHook(Enum):
    RIGHT = auto()
    LEFT = auto()


@dataclass
class BeamHint:
    break_depth: Optional[int] = None
    hook: Optional[BeamHook] = None


@dataclass
class BeamState:
    count: int
    break_depth: Optional[int] = None
    hook: Optional[BeamHook] = None


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
    hook: Optional[BeamHook] = None
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
                hook = BeamHook.RIGHT
        elif next_count is None:
            # Last item in group
            prev_count = cast(int, prev_count)
            if current_count > prev_count:
                hook = BeamHook.LEFT
        else:
            # Item in middle of group
            if current_count > prev_count and current_count > next_count:
                if prev_count < next_count:
                    hook = BeamHook.RIGHT
                elif prev_count > next_count:
                    hook = BeamHook.LEFT
                else:
                    # Surrounding positions flag counts are equal, so
                    # hook direction is ambiguous. Allow override.
                    hook = current_hint_hook or BeamHook.LEFT
        states.append(BeamState(current_count, break_depth, hook))
    return states
