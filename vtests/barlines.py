from helpers import render_vtest

from neoscore.common import *
from neoscore.core.flowable import Flowable
from neoscore.core.units import Mm
from neoscore.western import barline_style
from neoscore.western.barline import Barline
from neoscore.western.barline_style import BarlineStyle
from neoscore.western.staff import Staff

neoscore.setup()

flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
staff_1 = Staff((Mm(0), Mm(0)), flowable, Mm(150), Mm(2))
staff_2 = Staff((Mm(0), Mm(30)), flowable, Mm(150))
staff_3 = Staff((Mm(10), Mm(50)), flowable, Mm(150))

# test bar lines between stave 1 and 2
test_style = Barline(Mm(10), [staff_1, staff_2], barline_style.SINGLE)

for n, test_line in enumerate(barline_style.ALL_STYLES):

    Barline(Mm(10 * (n + 1) + 10), [staff_1, staff_2], styles=test_line)

test_double_dash = Barline(
    Mm(50),
    [staff_1, staff_3],
    (BarlineStyle(0.5, 1.0, pattern=PenPattern.DASH),
        BarlineStyle(0.5),
    ),
)

for n, test_line in enumerate(barline_style.ALL_STYLES):

    Barline(Mm(10 * (n + 1) + 80), [staff_1, staff_3], styles=test_line)

render_vtest("barlines")
