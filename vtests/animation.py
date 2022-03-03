import math
import os
import sys

from brown.common import *

brown.setup()


flowable = Flowable((Mm(0), Mm(0)), Mm(500), Mm(30), Mm(10))

staff = Staff((Mm(0), Mm(0)), Mm(500), flowable, Mm(1))
unit = staff.unit
clef = Clef(staff, unit(0), "treble")
KeySignature(clef.bounding_rect.width + unit(0.5), staff, "g_major")

OctaveLine((unit(20), unit(-4)), staff, unit(40))

note = Chordrest(unit(8), staff, ["e'''"], Beat(1, 4))


def refresh_func(time):
    brown._clear_interfaces()
    # Chordrests don't currently support mutability
    global note
    note.remove()
    note = Chordrest(unit(20) + Mm(math.sin(time) * 10), staff, ["e'''"], Beat(1, 4))
    brown.document._render()


brown.set_refresh_func(refresh_func)
brown.show()
