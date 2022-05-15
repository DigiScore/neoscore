from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.units import ZERO, Mm
from neoscore.western import notehead_tables
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff

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
