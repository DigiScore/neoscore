from helpers import render_example

from neoscore.common import *
from neoscore.core.flowable import Flowable
from neoscore.core.units import Mm
from neoscore.western import barline_style
from neoscore.western.barline import Barline
from neoscore.western.barline_style import BarlineStyle
from neoscore.western.staff import Staff

neoscore.setup()

flowable = Flowable((Mm(0), Mm(0)), None, Mm(200), Mm(30), Mm(5))
normal_staff = Staff((Mm(0), Mm(0)), flowable, Mm(150), line_spacing=Mm(2))
percussion_staff = Staff((Mm(0), Mm(30)), flowable, Mm(150), line_count=1)
offset_staff = Staff((Mm(10), Mm(50)), flowable, Mm(140))

all_staves = [normal_staff, percussion_staff, offset_staff]

# test barline across all staves
test_barline = Barline(Mm(10), all_staves)

# test barline spanning all staves
test_barline_2 = Barline(Mm(15), [normal_staff, offset_staff])

# test barline with DIY style unconnected
test_double_dash = Barline(
    Mm(20),
    all_staves,
    (
        BarlineStyle(0.3, 0.8),
        BarlineStyle(0.2, pattern=PenPattern.DASH),
    ),
    connected=False,
)

# test barline with DIY style and color change
test_double_color = Barline(
    Mm(30),
    all_staves,
    (
        BarlineStyle(0.2, 0.5, PenPattern.DASH, "#ff0000"),
        BarlineStyle(0.3, pattern=PenPattern.DASHDOTDOT, color="#006432"),
    ),
)

# end barline
end_line = Barline(Mm(150), all_staves, barline_style.END)

for n, test_line in enumerate(barline_style.ALL_STYLES):
    Barline(Mm(10 * (n + 1) + 30), all_staves, styles=test_line)

for n, test_line in enumerate(barline_style.ALL_STYLES):
    Barline(
        Mm(10 * (n + 1) + 60),
        [percussion_staff, offset_staff],
        styles=test_line,
        connected=False,
    )

# Tabs
tab_staff_1 = TabStaff((Mm(0), Mm(100)), flowable, Mm(150))
tab_staff_2 = TabStaff((Mm(0), Mm(120)), flowable, Mm(150), line_count=4)
all_tabs = [tab_staff_1, tab_staff_2]

test_tab = Barline(Mm(10), all_tabs, barline_style.THIN_DOUBLE)
for n, test_line in enumerate(barline_style.ALL_STYLES):
    Barline(Mm(10 * (n + 1) + 10), all_tabs, styles=test_line)

render_example("barlines")
