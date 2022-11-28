from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.units import ZERO, Mm
from neoscore.core.directions import DirectionY
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from neoscore.western.tuplet import Tuplet

neoscore.setup()

staff = Staff((Mm(10), Mm(10)), None, Mm(100))
clef = Clef(ZERO, staff, "treble")

note1 = Chordrest(Mm(5), staff, ["c"], (1, 8))
note2 = Chordrest(Mm(10), staff, None, (1, 8))
note3 = Chordrest(Mm(15), staff, ["d"], (1, 8))
note4 = Chordrest(Mm(20), staff, ["e"], (1, 8))
note5 = Chordrest(Mm(25), staff, None, (1, 8))

tuplet = Tuplet((Mm(0), Mm(-5)),
                note1,
                Mm(0),
                note5,
                "5:4",
                bracket_dir=DirectionY.UP)

note10 = Chordrest(Mm(50), staff, ["c'"], (1, 8))
note20 = Chordrest(Mm(60), staff, None, (1, 8))
note30 = Chordrest(Mm(65), staff, ["d'"], (1, 8))
note40 = Chordrest(Mm(70), staff, ["e'"], (1, 8))
note50 = Chordrest(Mm(75), staff, None, (1, 8))

tuplet = Tuplet((Mm(0), Mm(15)),
                note10,
                Mm(0),
                note50,
                "5:4")


neoscore.show()
