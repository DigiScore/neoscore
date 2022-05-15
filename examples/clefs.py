from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.units import ZERO, Mm
from neoscore.western import barline_style
from neoscore.western.barline import Barline
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.clef_type import CLEF_TYPE_SHORTHAND_NAMES
from neoscore.western.key_signature import KeySignature
from neoscore.western.staff import Staff
from neoscore.western.staff_group import StaffGroup

neoscore.setup()

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


Barline(staves[0].unit(35), staves, barline_style.THIN_DOUBLE)

render_example("clefs")
