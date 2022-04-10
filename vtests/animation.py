import math

from neoscore.common import *

neoscore.setup()

flowable = Flowable((Mm(0), Mm(0)), None, Mm(500), Mm(30), Mm(10))

staff = Staff((Mm(0), Mm(0)), flowable, Mm(500))
unit = staff.unit
clef = Clef(unit(0), staff, "treble")
KeySignature(clef.bounding_rect.width + unit(0.5), staff, "g_major")

center = unit(20)

n1 = Notehead(center, staff, "g'", Duration(1, 4))
n2 = Notehead(center, staff, "b'", Duration(1, 4))
n3 = Notehead(center, staff, "d''", Duration(1, 4))
n4 = Notehead(center, staff, "f''", Duration(1, 4))


def refresh_func(time):
    n1.x = center + Mm(math.sin((time / 2)) * 10)
    n2.x = center + Mm(math.sin((time / 2) + 1) * 12)
    n3.x = center + Mm(math.sin((time / 2) + 1.7) * 7)
    n4.x = center + Mm(math.sin((time / 2) + 2.3) * 15)


neoscore.show(refresh_func)
