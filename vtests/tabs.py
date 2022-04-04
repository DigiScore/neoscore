from neoscore.common import *

neoscore.setup()


# 6 line tab

staff_1 = TabStaff(ORIGIN, None, Mm(100))
clef_1 = TabClef(ZERO, staff_1)

TabNumber(Mm(5), staff_1, 1, 1)
TabNumber(Mm(7), staff_1, 1, 2)
TabNumber(Mm(7), staff_1, 2, 1)
TabNumber(Mm(7), staff_1, 3, 1)
TabNumber(Mm(7), staff_1, 4, 2)
TabNumber(Mm(7), staff_1, 5, 3)
TabNumber(Mm(7), staff_1, 6, 0)
TabNumber(Mm(10), staff_1, 1, 9)


# 4 line tab

staff_2 = TabStaff((ZERO, Mm(20)), None, Mm(100), line_count=4)
clef_2 = TabClef(ZERO, staff_2, "4stringTabClef")


regular_staff = Staff((ZERO, Mm(40)), None, Mm(100))
Clef(ZERO, regular_staff, "treble")

all_staves = [staff_1, staff_2, regular_staff]

Barline(Mm(20), all_staves)

neoscore.show()
