from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.point import ORIGIN
from neoscore.core.units import ZERO, Mm
from neoscore.western.arpeggio_line import ArpeggioLine
from neoscore.western.barline import Barline
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from neoscore.western.staff_group import StaffGroup
from neoscore.western.tab_clef import TabClef
from neoscore.western.tab_number import TabNumber
from neoscore.western.tab_staff import TabStaff

neoscore.setup()

flowable = Flowable(ORIGIN, None, Mm(500), Mm(60))

staff_group = StaffGroup()

# 6 line tab

staff_1 = TabStaff(ORIGIN, flowable, Mm(500), staff_group)
clef_1 = TabClef(staff_1)

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
clef_2 = TabClef(staff_2, "4stringTabClef")


regular_staff = Staff((ZERO, Mm(35)), flowable, Mm(500), staff_group)
Clef(ZERO, regular_staff, "treble")

all_staves = [staff_1, staff_2, regular_staff]

Barline(Mm(22), all_staves)

render_example("tabs")
