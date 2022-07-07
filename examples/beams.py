from typing import List, NamedTuple, Optional

from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.directions import DirectionX, DirectionY
from neoscore.core.units import ZERO, Mm
from neoscore.western.beam_group import BeamGroup
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.duration import DurationDef
from neoscore.western.pitch import PitchDef
from neoscore.western.staff import Staff

neoscore.setup()


class TestChord(NamedTuple):
    pitches: Optional[List[PitchDef]]
    duration: DurationDef
    stem_direction: Optional[DirectionY] = None
    beam_break_depth: Optional[int] = None
    beam_hook_dir: Optional[DirectionX] = None


staff_y = ZERO


def create_example(chords: List[TestChord], direction: Optional[DirectionY] = None):
    global staff_y
    staff = Staff((ZERO, staff_y), None, Mm(150))
    staff_y = staff.y
    Clef(ZERO, staff, "treble")
    unit = staff.unit
    group = []
    spacing = unit(6)
    for i, c in enumerate(chords):
        group.append(
            Chordrest(
                unit(7) + (spacing * i),
                staff,
                c.pitches,
                c.duration,
                stem_direction=c.stem_direction,
                beam_break_depth=c.beam_break_depth,
                beam_hook_dir=c.beam_hook_dir,
            )
        )
    BeamGroup(group, direction)
    staff_y += Mm(24)


# Flat beams

create_example(
    [
        TestChord(["f"], (1, 8)),
        TestChord(["f"], (1, 8)),
    ]
)

create_example(
    [
        TestChord(["f"], (1, 8)),
        TestChord(["f"], (1, 8)),
        TestChord(["f"], (1, 16)),
        TestChord(["f"], (1, 16)),
        TestChord(["f"], (1, 32)),
        TestChord(["f"], (1, 32)),
    ]
)

create_example(
    [
        TestChord(["f'"], (3, 16)),
        TestChord(["f'"], (1, 16)),
    ]
)


create_example(
    [
        TestChord(["f"], (1, 32)),
        TestChord(["f"], (1, 32), beam_break_depth=1),
        TestChord(["f"], (1, 32)),
        TestChord(["f"], (1, 32)),
    ]
)

# Hook direction overrides

create_example(
    [
        TestChord(["f"], (1, 8)),
        TestChord(["f"], (1, 16)),
        TestChord(["f"], (1, 8)),
    ]
)

create_example(
    [
        TestChord(["f"], (1, 8)),
        TestChord(["f"], (1, 16), beam_hook_dir=DirectionX.RIGHT),
        TestChord(["f"], (1, 8)),
    ]
)

# Beam direction override

create_example(
    [
        TestChord(["a"], (1, 8)),
        TestChord(["a"], (1, 16)),
        TestChord(["a"], (1, 8)),
    ],
    DirectionY.DOWN,
)


# Angled beams

create_example(
    [
        TestChord(["f"], (1, 32)),
        TestChord(["f"], (1, 32), beam_break_depth=1),
        TestChord(["f"], (1, 32)),
        TestChord(["g'"], (1, 32)),
        TestChord(["c#"], (3, 16)),
        TestChord(["d"], (1, 16)),
    ]
)

create_example(
    [
        TestChord(["bb'", "e'"], (1, 32)),
        TestChord(["f"], (1, 32), beam_break_depth=2),
        TestChord(["f"], (1, 32)),
        TestChord(["g'"], (1, 32)),
        TestChord(["c#"], (3, 16)),
        TestChord(["e'"], (1, 32)),
        TestChord(["eb'"], (1, 32)),
        TestChord(["d'"], (1, 8)),
    ]
)

render_example("beams")
