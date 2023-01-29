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


# 3 stroke tremolo on single Chordrest
c1 = Chordrest(Mm(10), staff, ["c'"], (1, 2))
Tremolo.for_chordrest(c1, 3)

# pendereckiTremolo
c2 = Chordrest(Mm(20), staff, ["d"], (1, 2))
Tremolo.for_chordrest(c2, "pendereckiTremolo")

# 2 stroke tremolo on a whole note
c3 = Chordrest(Mm(30), staff, ["b'"], (1, 1))
Tremolo.for_chordrest(c3, 2)

# 4 stroke tremolo on a chord with many notes and a flag
c4 = Chordrest(Mm(40), staff, ["b'", "c", "d#"], (1, 32))
Tremolo.for_chordrest(c4, 2)

# 5 stroke tremolo bridging two Chordrests
# But note that for best results, you should manually construct tremolos
# spanning chordrests by drawing `Beam` objects.
c5 = Chordrest(Mm(50), staff, ["d'"], (1, 4))
c6 = Chordrest(Mm(60), staff, ["g"], (1, 4))
Tremolo((Mm(5), Mm(5)), c5, 5)


render_example("tremolo")
