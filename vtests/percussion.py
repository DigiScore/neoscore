from helpers import render_vtest

from neoscore.common import *

neoscore.setup()

# 1 line staff

staff_1 = Staff((Mm(0), Mm(10)), None, Mm(100), line_count=1)
clef = Clef(Mm(0), staff_1, "percussion_1")
Chordrest(Mm(10), staff_1, ["c"], (1, 8), table=notehead_tables.SLASH)
Chordrest(Mm(20), staff_1, None, (1, 32))

# 3 line staff

staff_2 = Staff((ZERO, Mm(30)), None, Mm(100), line_count=3)
clef = Clef(Mm(0), staff_2, "percussion_2")
Chordrest(Mm(10), staff_2, ["c"], (1, 8), table=notehead_tables.X)

render_vtest("percussion")
