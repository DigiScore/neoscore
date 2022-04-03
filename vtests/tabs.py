from neoscore.common import *

neoscore.setup()


# 6 line tab

staff_1 = TabStaff(ORIGIN, None, Mm(100))
clef_1 = TabClef(ZERO, staff_1)

# Mockup for something that will probably be pulled into tab code
def add_fingering(x, string, finger):
    string_y = staff_1.string_y(string)
    mt = MusicText(
        (x, ZERO),
        staff_1,
        f"fingering{finger}",
        background_brush=neoscore.background_brush,
    )
    mt.y = string_y + (mt.bounding_rect.height / 2)


add_fingering(Mm(5), 1, 1)
add_fingering(Mm(7), 1, 2)
add_fingering(Mm(7), 2, 1)
add_fingering(Mm(7), 3, 1)
add_fingering(Mm(7), 4, 2)
add_fingering(Mm(7), 5, 3)
add_fingering(Mm(7), 6, 0)
add_fingering(Mm(10), 1, 5)


# 4 line tab

staff_2 = TabStaff((ZERO, Mm(20)), None, Mm(100), line_count=4)
clef_2 = TabClef(ZERO, staff_2, "4stringTabClef")


regular_staff = Staff((ZERO, Mm(40)), None, Mm(100))
Clef(ZERO, regular_staff, "treble")

all_staves = [staff_1, staff_2, regular_staff]

Barline(Mm(20), all_staves)

neoscore.show()
