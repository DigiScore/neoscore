from neoscore.common import *
from neoscore.western.clef_type import CLEF_TYPE_SHORTHAND_NAMES

neoscore.setup()
from helpers import render_example

staff_group = StaffGroup()
staves = []

for (i, clef_type) in enumerate(CLEF_TYPE_SHORTHAND_NAMES.values()):
    staff = Staff((Mm(20), Mm(i * 30)), None, Mm(100), staff_group)
    staves.append(staff)
    unit = staff.unit
    clef = Clef(ZERO, staff, clef_type)
    KeySignature(ZERO, staff, "cs_major")
    Chordrest(unit(0), staff, ["c,,"], (1, 4))
    Chordrest(unit(5), staff, ["c,"], (1, 4))
    Chordrest(unit(10), staff, ["c"], (1, 4))
    Chordrest(unit(15), staff, ["c'"], (1, 4))
    KeySignature(unit(20), staff, "cf_major")


Barline(unit(35), staves, barline_style.THIN_DOUBLE)

render_example("clefs")
