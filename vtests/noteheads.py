from helpers import render_vtest

from neoscore.common import *

neoscore.setup()


for (i, table) in enumerate(notehead_tables.ALL_TABLES):
    staff = Staff((Mm(0), Mm(i * 10)), None, Mm(100))
    unit = staff.unit
    clef = Clef(unit(0), staff, "treble")
    KeySignature(clef.bounding_rect.width + unit(0.5), staff, "c_major")
    Chordrest(unit(10), staff, ["c'"], (2, 1), notehead_table=table)
    Chordrest(unit(15), staff, ["c'"], (1, 1), notehead_table=table)
    Chordrest(unit(20), staff, ["c'"], (1, 2), notehead_table=table)
    Chordrest(unit(25), staff, ["c'"], (1, 4), notehead_table=table)
    Chordrest(unit(30), staff, ["c'"], (1, 8), notehead_table=table)
    Chordrest(unit(35), staff, ["c'"], (1, 16), notehead_table=table)
    Chordrest(unit(40), staff, ["c'"], (1, 32), notehead_table=table)
    Chordrest(unit(45), staff, ["c'"], (1, 64), notehead_table=table)

render_vtest("noteheads")
