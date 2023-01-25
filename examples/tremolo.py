from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.point import ZERO
from neoscore.core.units import Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from neoscore.western.tremolo import Tremolo

neoscore.setup()

staff = Staff((Mm(10), Mm(10)), None, Mm(150))
clef = Clef(ZERO, staff, "treble")

c1 = Chordrest(Mm(10), staff, ["c'"], (1, 2))
c2 = Chordrest(Mm(20), staff, ["d"], (1, 2))
c3 = Chordrest(Mm(30), staff, [], (1, 4))
c4 = Chordrest(Mm(50), staff, ["d'"], (1, 4))
c5 = Chordrest(Mm(60), staff, ["g"], (1, 4))

# 3 stroke tremolo on single Chordrest
Tremolo.for_chordrest(c1, 3)

# pendereckiTremolo
Tremolo.for_chordrest(c2, "pendereckiTremolo")

# 2 stroke tremolo on a rest (don't know how you would play that :)
Tremolo.for_chordrest(c3, 2)

# 5 sroke tremolo bridging two Chordrests
Tremolo((Mm(5), Mm(5)), c4, 5)


render_example("tremolo")
