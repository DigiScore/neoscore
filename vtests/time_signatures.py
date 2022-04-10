from helpers import render_vtest

from neoscore.common import *
from neoscore.western.meter import MeterDef

neoscore.setup()


staff = Staff(ORIGIN, None, Mm(150))

meters: list[MeterDef] = [
    COMMON_TIME,
    CUT_TIME,
    (3, 4),
    (5, 16),
    (12, 16),
    (12, 8),
    ([3, 2, 3], 8),
]


for (i, meter) in enumerate(meters):
    TimeSignature(Mm(i * 15), staff, meter)

render_vtest("time_signature")
