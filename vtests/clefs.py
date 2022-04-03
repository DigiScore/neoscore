from neoscore.common import *
from neoscore.western.clef_type import CLEF_TYPE_SHORTHAND_NAMES

neoscore.setup()

staves = []

for (i, clef_type) in enumerate(CLEF_TYPE_SHORTHAND_NAMES.values()):
    staff = Staff((Mm(0), Mm(i * 15)), None, Mm(100))
    staves.append(staff)
    unit = staff.unit
    clef = Clef(unit(0), staff, clef_type)
    KeySignature(clef.bounding_rect.width + unit(0.5), staff, "cs_major")
    Chordrest(unit(15), staff, ["c,"], (1, 4))
    Chordrest(unit(20), staff, ["c"], (1, 4))
    Chordrest(unit(25), staff, ["c'"], (1, 4))
    Chordrest(unit(30), staff, ["c''"], (1, 4))
    KeySignature(unit(37), staff, "cf_major")


Barline(unit(35), staves)
Barline(unit(35.5), staves)

neoscore.show()
