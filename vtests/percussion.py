from neoscore.common import *

neoscore.setup()

# 1 line staff

staff_1 = Staff(ORIGIN, None, Mm(100), line_count=1)
clef = Clef(Mm(0), staff_1, "percussion_1")
Chordrest(Mm(5), staff_1, ["c'"], (1, 8), notehead_table=notehead_tables.SLASH)

# 3 line staff

staff_2 = Staff((ZERO, Mm(20)), None, Mm(100), line_count=3)
clef = Clef(Mm(0), staff_2, "percussion_2")
Chordrest(Mm(5), staff_2, ["c'"], (1, 8), notehead_table=notehead_tables.X)

neoscore.show()
