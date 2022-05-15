import math

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.units import ZERO, Mm
from neoscore.western.clef import Clef
from neoscore.western.duration import Duration
from neoscore.western.key_signature import KeySignature
from neoscore.western.notehead import Notehead
from neoscore.western.staff import Staff

neoscore.setup()

flowable = Flowable((Mm(0), Mm(0)), None, Mm(500), Mm(30), Mm(10))

staff = Staff((Mm(0), Mm(0)), flowable, Mm(500))
unit = staff.unit
clef = Clef(ZERO, staff, "treble")
KeySignature(ZERO, staff, "g_major")

center = unit(15)

n1 = Notehead(center, staff, "g", Duration(1, 4))
n2 = Notehead(center, staff, "b", Duration(1, 4))
n3 = Notehead(center, staff, "d'", Duration(1, 4))
n4 = Notehead(center, staff, "f'", Duration(1, 4))


def refresh_func(time):
    n1.x = center + Mm(math.sin((time / 2)) * 10)
    n2.x = center + Mm(math.sin((time / 2) + 1) * 12)
    n3.x = center + Mm(math.sin((time / 2) + 1.7) * 7)
    n4.x = center + Mm(math.sin((time / 2) + 2.3) * 15)


if __name__ == "__main__":
    neoscore.show(refresh_func)
