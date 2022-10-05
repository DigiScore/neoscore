import random
from typing import Optional

from neoscore.core import neoscore
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.invisible_clef import InvisibleClef
from neoscore.western.staff import Staff

"""
This example demonstrates how simple recursive systems can be used to build fractal
scores with neoscore. This leverages neoscore's rotation and scaling system to create a
simple Fractal Canopy (https://en.wikipedia.org/wiki/Fractal_canopy) using staves
instead of lines. The staves are populated with a simple random note generator.
"""

neoscore.setup()

INITIAL_LENGTH = Mm(100)
LENGTH_STEP = Mm(10)
SCALE_STEP = 0.8
BRANCH_ANGLE = 35

pitches = [
    "f,",
    "a,",
    "c",
    "e",
    "f",
    "g",
    "a",
    "c'",
    "e'",
    "f'",
    "a'",
    "b",
    "c''",
    "e''",
    "f''",
]
durations = [
    (1, 4),
    (1, 2),
]


def populate_staff(staff: Staff):
    # Draw the clef only on the root staff
    if isinstance(staff.parent, Staff):
        InvisibleClef(ZERO, staff, "treble")
    else:
        Clef(ZERO, staff, "treble")
    current_x = ZERO
    max_x = staff.breakable_length - Mm(5)
    while current_x < max_x:
        pitch = random.choice(pitches)
        duration = random.choice(durations)
        Chordrest(current_x, staff, [pitch], duration)
        current_x += Mm(random.uniform(2, 30))


def draw_staff(parent: Optional[Staff], length: Unit, angle: float) -> Staff:
    if parent:
        pos = Point(parent.breakable_length, ZERO)
    else:
        pos = ORIGIN
    s = Staff(pos, parent, length)
    s.rotation = angle
    s.scale = SCALE_STEP
    populate_staff(s)
    return s


def draw_tree(branch_length: Unit, last_staff: Optional[Staff], angle: float):
    if branch_length > Mm(5):
        trunk = draw_staff(last_staff, branch_length, angle)
        draw_tree(branch_length - LENGTH_STEP, trunk, BRANCH_ANGLE)
        draw_tree(branch_length - LENGTH_STEP, trunk, -BRANCH_ANGLE)


draw_tree(INITIAL_LENGTH, None, -90)

neoscore.show(display_page_geometry=False)
