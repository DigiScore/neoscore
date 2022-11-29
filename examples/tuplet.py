from neoscore.core import neoscore
from neoscore.core.directions import DirectionY
from neoscore.core.units import ZERO, Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from neoscore.western.tuplet import Tuplet

neoscore.setup()

staff = Staff((Mm(10), Mm(10)), None, Mm(150))
clef = Clef(ZERO, staff, "treble")

# straight tuplet indicator
note1 = Chordrest(Mm(5), staff, ["c"], (1, 8))
note2 = Chordrest(Mm(10), staff, None, (1, 8))
note3 = Chordrest(Mm(15), staff, ["d"], (1, 8))
note4 = Chordrest(Mm(20), staff, ["e"], (1, 8))
note5 = Chordrest(Mm(25), staff, None, (1, 8))

Tuplet((Mm(0), Mm(-2)), note1, (Mm(115), Mm(-2)), note5, "4", bracket_dir=DirectionY.UP)

# sloping under tuplet indicator
note10 = Chordrest(Mm(50), staff, ["c'"], (1, 4))
note20 = Chordrest(Mm(60), staff, None, (1, 8))
note30 = Chordrest(Mm(65), staff, ["d'"], (1, 8))
note40 = Chordrest(Mm(70), staff, ["e'"], (1, 8))
note50 = Chordrest(Mm(75), staff, None, (1, 8))

Tuplet((Mm(0), Mm(15)), note10, (Mm(130), Mm(250)), note50, "6:4")

# sloping top tuplet indicator
note11 = Chordrest(Mm(105), staff, ["c"], (1, 8))
note21 = Chordrest(Mm(110), staff, None, (1, 8))
note31 = Chordrest(Mm(115), staff, ["d"], (1, 8))
note41 = Chordrest(Mm(120), staff, ["e"], (1, 8))
note51 = Chordrest(Mm(125), staff, None, (1, 8))

Tuplet(
    (Mm(0), Mm(5)), note11, (Mm(215), Mm(-22)), note51, "5:4", bracket_dir=DirectionY.UP
)


neoscore.show(display_page_geometry=False)
