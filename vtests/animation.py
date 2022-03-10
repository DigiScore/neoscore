import math

from brown.common import *

brown.setup()

flowable = Flowable((Mm(0), Mm(0)), Mm(500), Mm(30), Mm(10))

staff = Staff((Mm(0), Mm(0)), Mm(500), flowable, Mm(1))
unit = staff.unit
clef = Clef(staff, unit(0), "treble")
KeySignature(clef.bounding_rect.width + unit(0.5), staff, "g_major")

center = unit(20)

n1 = Notehead(center, "g'", Beat(1, 4), staff)
n2 = Notehead(center, "b'", Beat(1, 4), staff)
n3 = Notehead(center, "d''", Beat(1, 4), staff)
n4 = Notehead(center, "f''", Beat(1, 4), staff)


def refresh_func(time):
    n1.x = center + Mm(math.sin((time / 2)) * 10)
    n2.x = center + Mm(math.sin((time / 2) + 1) * 12)
    n3.x = center + Mm(math.sin((time / 2) + 1.7) * 7)
    n4.x = center + Mm(math.sin((time / 2) + 2.3) * 15)


brown.show(refresh_func)
