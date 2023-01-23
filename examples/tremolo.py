from neoscore.common import *
from neoscore.western.tremolo import Tremolo

neoscore.setup()

staff = Staff((Mm(10), Mm(10)), None, Mm(150))
clef = Clef(ZERO, staff, "treble")

c1 = Chordrest(Mm(10), staff, ["c'"], (1, 2))
c2 = Chordrest(Mm(20), staff, ["c"], (1, 2))
c3 = Chordrest(Mm(30), staff, [], (1, 4))
c4 = Chordrest(Mm(50), staff, ["d"], (1, 4))
c5 = Chordrest(Mm(60), staff, ["g"], (1, 4))

Tremolo.for_chordrest(c1, 3)
Tremolo.for_chordrest(c2, 2)
Tremolo.for_chordrest(c3, 1)
Tremolo((Mm(5), Mm(0)), c4, 5)

neoscore.show(display_page_geometry=False)
