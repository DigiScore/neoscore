from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.point import ORIGIN
from neoscore.core.units import ZERO, Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.notehead import Notehead
from neoscore.western.slur import Slur
from neoscore.western.staff import Staff
from neoscore.western.tie import Tie

neoscore.setup()

staff = Staff((Mm(10), Mm(10)), None, Mm(150))
clef = Clef(ZERO, staff, "treble")

# slur
note1 = Chordrest(Mm(10), staff, ["c'"], (1, 4))
note2 = Chordrest(Mm(20), staff, ["f'"], (1, 4))
slur = Slur((Mm(0), Mm(0)), note1, (Mm(0), Mm(-5)), note2)

note3 = Chordrest(Mm(30), staff, ["d'"], (1, 4))
note4 = Chordrest(Mm(40), staff, ["d'"], (1, 4))
tie = Tie((Mm(0), Mm(0)), note3, Mm(10))

nh1 = Notehead(Mm(60), staff, "e", (1, 4))
nh2 = Notehead(Mm(80), staff, "b", (1, 4))
Tie(ORIGIN, nh1, Mm(20))

render_example("slur_tie")
