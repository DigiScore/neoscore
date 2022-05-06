from helpers import render_example

from neoscore.common import *

neoscore.setup()


length = Mm(2000)
flowable = Flowable((Mm(50), ZERO), None, length, Mm(70))

group = StaffGroup()

staff_1 = Staff(ORIGIN, flowable, length, group)
Clef(ZERO, staff_1, "treble")
KeySignature(ZERO, staff_1, "cf_major")
TimeSignature(ZERO, staff_1, ([3, 3, 2], 8))
Chordrest(ZERO, staff_1, "b", (1, 32))

staff_2 = Staff((ZERO, Mm(15)), flowable, length, group)
Clef(ZERO, staff_2, "bass")
KeySignature(ZERO, staff_2, "cf_major")
TimeSignature(ZERO, staff_2, ([3, 3, 2], 8))

staff_3 = TabStaff((ZERO, Mm(30)), flowable, length, group)
TabClef(ZERO, staff_3)
TabNumber(ZERO, staff_3, 3, 123)

staff_4 = Staff((ZERO, Mm(50)), flowable, length, group, line_count=1)
Clef(ZERO, staff_4, "percussion_1")
TimeSignature(ZERO, staff_4, ([3, 3, 2], 8))

staves = [staff_1, staff_2, staff_3, staff_4]

SystemLine(ZERO, staves)
Brace(ZERO, staves)

Barline(Mm(30), staves)


render_example("staff_systems")
