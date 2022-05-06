from helpers import render_example

from neoscore.common import *

neoscore.setup()

flowable = Flowable(ORIGIN, None, Mm(500), Mm(60))

staff_group = StaffGroup()

# 6 line tab

staff_1 = TabStaff(ORIGIN, flowable, Mm(500), staff_group)
clef_1 = TabClef(ZERO, staff_1)

TabNumber(Mm(0), staff_1, 1, 1)
TabNumber(Mm(5), staff_1, 1, 2)
TabNumber(Mm(5), staff_1, 2, 1)
TabNumber(Mm(5), staff_1, 3, 1)
TabNumber(Mm(5), staff_1, 4, 2)
TabNumber(Mm(5), staff_1, 5, 3)
TabNumber(Mm(5), staff_1, 6, 0)
TabNumber(Mm(8), staff_1, 1, 9)
TabNumber(Mm(15), staff_1, 4, 123)

# Rolled chord

chord_notes = [
    TabNumber(Mm(30), staff_1, 1, 2),
    TabNumber(Mm(30), staff_1, 2, 1),
    TabNumber(Mm(30), staff_1, 3, 1),
    TabNumber(Mm(30), staff_1, 4, 2),
    TabNumber(Mm(30), staff_1, 5, 3),
]
u = staff_1.unit
arp = ArpeggioLine(
    (u(-1.5), u(-1)), chord_notes[0], (u(-1.5), u(1.5)), chord_notes[-1], True
)


# 4 line tab

staff_2 = TabStaff((ZERO, Mm(20)), flowable, Mm(500), staff_group, line_count=4)
clef_2 = TabClef(ZERO, staff_2, "4stringTabClef")


regular_staff = Staff((ZERO, Mm(35)), flowable, Mm(500), staff_group)
Clef(ZERO, regular_staff, "treble")

all_staves = [staff_1, staff_2, regular_staff]

Barline(Mm(22), all_staves)

render_example("tabs")
