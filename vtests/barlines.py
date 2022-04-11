from neoscore.common import *
from neoscore.core.flowable import Flowable
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.core.point import Point
from neoscore.core.units import Mm
from neoscore.western.barline import Barline
from neoscore.western.staff import Staff
from neoscore.western import barline_style

neoscore.setup()

flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
staff_1 = Staff((Mm(0), Mm(0)), flowable, Mm(100), Mm(2))
staff_2 = Staff((Mm(0), Mm(30)), flowable, Mm(100))
staff_3 = Staff((Mm(10), Mm(50)), flowable, Mm(100))

# barline = Barline(Mm(15), [staff_1, staff_2])
barline_end = Barline(Mm(30),
                      [staff_1, staff_2],
                      style=barline_style.END
                      )

neoscore.show()




