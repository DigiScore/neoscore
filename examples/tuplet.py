from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.units import ZERO, Mm
from neoscore.western import notehead_tables
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from neoscore.western.tuplet import Tuplet

neoscore.setup()

staff = Staff((Mm(10), Mm(10)), None, Mm(100))
clef = Clef(ZERO, staff, "treble")

note1 = Chordrest(Mm(5), staff, ["c'"], (1, 8))
note2 = Chordrest(Mm(10), staff, None, (1, 8))
note3 = Chordrest(Mm(15), staff, ["d'"], (1, 8))
note4 = Chordrest(Mm(20), staff, ["e'"], (1, 8))
note5 = Chordrest(Mm(25), staff, None, (1, 8))

tuplet = Tuplet((Mm(0), Mm(10)),
                note1,
                (Mm(0), Mm(10)),
                note5,
                "5:4")

neoscore.show()
