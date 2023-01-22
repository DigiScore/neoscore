from neoscore.common import *
from neoscore.western.tremolo import Tremolo

neoscore.setup()

staff = Staff((Mm(10), Mm(10)), None, Mm(150))
clef = Clef(ZERO, staff, "treble")

c1 = Chordrest(Mm(10), staff, ["a", "c"], (1, 2))
c2 = Chordrest(Mm(20), staff, ["c"], (1, 2))
c3 = Chordrest(Mm(40), staff, ["a,"], (1, 4))
c4 = Chordrest(Mm(50), staff, ["c", "g"], (1, 1))
c5 = Chordrest(Mm(60), staff, ["c"], (1, 2))
c6 = Chordrest(Mm(80), staff, ["c", "e"], (1, 2))
c7 = Chordrest(Mm(90), staff, ["e", "g"], (1, 2))
# target_notehead = c.highest_notehead


Tremolo(c1, 3)
Tremolo(c2, 2)
Tremolo(c3, 1)
Tremolo(c4, 4)
Tremolo(c5, alt_glyph="pendereckiTremolo")
Tremolo(c6, 4, c7)


# Tremolo(parent=c,
#     strokes=1,
# end_pos=ORIGIN,
# end_parent=c1,
# alt_glyph="pendereckiTremolo",
#     )


neoscore.show(display_page_geometry=False)
