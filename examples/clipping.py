from helpers import render_example

from neoscore.common import *
from neoscore.core.units import ZERO

neoscore.setup()

flowable = Flowable((Mm(0), Mm(0)), None, Mm(2000), Mm(30), Mm(10))

staff = Staff((Mm(0), Mm(0)), flowable, Mm(2000), line_spacing=Mm(1))

# If staff is longer than flowable, the last line runs to the end.
# this behavior kind of makes sense, actually..

unit = staff.unit
clef = Clef(unit(0), staff, "treble")
KeySignature(clef.bounding_rect.width + unit(0.5), staff, "g_major")

mt = MusicText((Mm(165), staff.unit(4)), staff, ("gClef", 1), scale=4)

w = MusicText((Mm(240), staff.unit(2)), staff, ["gClef"] * 100)

p = Path.straight_line((ZERO, Mm(-10)), w, end=(w.breakable_length, ZERO))

render_example("clipping")
