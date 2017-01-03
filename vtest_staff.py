#!/usr/bin/env python3

from brown.core import brown
from brown.utils.units import Mm
from brown.core.flowable_frame import FlowableFrame
from brown.primitives.staff import Staff
from brown.primitives.clef import Clef
from brown.core.glyph import Glyph


brown.setup()

# Test hacky use of flowable coordinate space
flow = FlowableFrame((Mm(0), Mm(0)), Mm(35000), Mm(20), Mm(10))
flow.render()

# glyph = Glyph((Mm(0), Mm(10)), "H", parent=flow)
# glyph.render()
# glyph2 = Glyph((Mm(1000), Mm(10)), "I", parent=flow)
# glyph2.render()
staff = Staff((Mm(0), Mm(0)), Mm(2000), flow, Mm(1))
staff.render()

# clef = Clef(staff, Mm(0), 'treble')
# clef.render()
for i in range(100):
    Clef(staff, Mm(i*5), 'treble').render()

brown.show()
