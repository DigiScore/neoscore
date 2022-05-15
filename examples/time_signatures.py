from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.units import ZERO, Mm
from neoscore.western.meter import COMMON_TIME, CUT_TIME, MeterDef
from neoscore.western.staff import Staff
from neoscore.western.time_signature import TimeSignature

neoscore.setup()


staff = Staff((Mm(10), ZERO), None, Mm(150))

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

render_example("time_signature")
