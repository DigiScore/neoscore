from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, cast

from neoscore.models.duration_display import DurationDisplay

# wip sketching...


# @dataclass
# class BeamGroup:


# I think this algorithm actually doesn't even need to know the real
# duration values - it just needs to know flag counts.


class BeamHook(Enum):
    NONE = auto()
    RIGHT = auto()
    LEFT = auto()


@dataclass
class BeamState:
    count: int
    hook: BeamHook = BeamHook.NONE
    break_depth: Optional[int] = None


def resolve_beams(durs: list[DurationDisplay]) -> list[BeamState]:
    if len(durs) < 2:
        raise ValueError("Beam groups must have at least 2 members")
    states: list[BeamState] = []
    beam_counts = [dur.flag_count for dur in durs]  # assume all durs have flags
    for i, current_count in enumerate(beam_counts):
        prev_count = beam_counts[i - 1] if i > 0 else None
        next_count = beam_counts[i + 1] if i < len(beam_counts) - 1 else None
        hook = BeamHook.NONE
        if prev_count is None:
            # First item in group
            next_count = cast(int, next_count)
            if next_count < current_count:
                hook = BeamHook.RIGHT
        elif next_count is None:
            # Last item in group
            if prev_count < current_count:
                hook = BeamHook.LEFT
        else:
            # Item in middle of group
            if current_count > prev_count and current_count > next_count:
                hook = BeamHook.LEFT
        states.append(BeamState(current_count, hook))
    return states
