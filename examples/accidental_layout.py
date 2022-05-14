"""
This is mostly for testing purposes demonstrating the shortcomings of our current
accidental layout algorithm. See https://github.com/DigiScore/neoscore/issues/32
"""

from helpers import render_example

from neoscore.common import *

neoscore.setup()


flowable = Flowable(ORIGIN, None, Mm(500), Mm(30))
staff = Staff(ORIGIN, flowable, Mm(500))
Clef(ZERO, staff, "treble")

# A single accidental looks good
Chordrest(Mm(10), staff, ["bf"], (1, 4))
Barline(Mm(15), [staff])

# Two adjacent accidentals look OK
Chordrest(Mm(25), staff, ["f#", "gn"], (1, 8))
Chordrest(Mm(40), staff, ["gb", "ab"], (1, 8))
Chordrest(Mm(55), staff, ["dbb'", "ebb'"], (1, 8))
Chordrest(Mm(70), staff, ["bb", "db'"], (1, 8))
Barline(Mm(75), [staff])

# Bounding rect cutouts are not respected, most apparent in flats a 4th or 5th apart.
Chordrest(Mm(85), staff, ["bb", "eb'"], (1, 8))
Chordrest(Mm(100), staff, ["ab", "eb'"], (1, 8))
Barline(Mm(105), [staff])

# More than 2 colliding notes do not look good
Chordrest(Mm(115), staff, ["g#", "a#", "b#"], (1, 8))
Chordrest(Mm(130), staff, ["gb", "an", "bb"], (1, 8))
Barline(Mm(105), [staff])

render_example("accidental_layout")
