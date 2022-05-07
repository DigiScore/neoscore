from helpers import render_example

from neoscore.common import *

neoscore.setup()

# 1 line staff

staff_1 = Staff((Mm(10), Mm(10)), None, Mm(100), line_count=1)
clef = Clef(ZERO, staff_1, "percussion_1")
Chordrest(Mm(5), staff_1, ["c"], (1, 8), table=notehead_tables.SLASH)
Chordrest(Mm(10), staff_1, None, (1, 32))

# 3 line staff

staff_2 = Staff((Mm(10), Mm(30)), None, Mm(100), line_count=3)
clef = Clef(ZERO, staff_2, "percussion_2")
Chordrest(Mm(5), staff_2, ["c"], (1, 8), table=notehead_tables.X)

render_example("percussion")
