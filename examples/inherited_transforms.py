from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.point import ORIGIN
from neoscore.core.text import Text
from neoscore.core.units import ZERO, Mm
from neoscore.western.barline import Barline
from neoscore.western.beam_group import BeamGroup
from neoscore.western.brace import Brace
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.key_signature import KeySignature
from neoscore.western.staff import Staff
from neoscore.western.staff_group import StaffGroup
from neoscore.western.system_line import SystemLine
from neoscore.western.time_signature import TimeSignature

neoscore.setup()

# Build a chain of simple text objects inheriting incremental scaling and rotations

prev = Text((ZERO, Mm(20)), None, "root")

for i in range(1, 5):
    prev = Text((Mm(20), ZERO), prev, f"desc_{i}", scale=1.1, rotation=5)

# Build a much more complex object - a populated staff system, and rotate it

parent = Text((Mm(50), Mm(100)), None, "parent", rotation=-15)

group = StaffGroup()

staff_1 = Staff(ORIGIN, parent, Mm(100), group)
Clef(ZERO, staff_1, "treble")
KeySignature(ZERO, staff_1, "ef_minor")
TimeSignature(ZERO, staff_1, (3, 4))
Chordrest(ZERO, staff_1, ["b"], (1, 32))

staff_2 = Staff((ZERO, Mm(15)), parent, Mm(110), group)
Clef(ZERO, staff_2, "bass")
KeySignature(ZERO, staff_2, "ef_minor")
TimeSignature(ZERO, staff_2, ([3, 3, 2], 8))

BeamGroup(
    [
        Chordrest(Mm(32), staff_2, ["c"], (1, 8)),
        Chordrest(Mm(38), staff_2, ["dn"], (1, 16)),
        Chordrest(Mm(42), staff_2, ["e"], (1, 16)),
    ]
)


staves = [staff_1, staff_2]

SystemLine(staves)
Brace(staves)

Barline(Mm(30), staves)

render_example("inherited_transforms")
