from helpers import render_example

from neoscore.common import *

neoscore.setup()

flowable = Flowable(ORIGIN, None, Mm(400), Mm(30))
staff_1 = Staff(ORIGIN, flowable, Mm(400))
staff_2 = Staff((ZERO, Mm(15)), flowable, Mm(400))
SystemLine(ZERO, [staff_1, staff_2])


render_example("doc-testing")
