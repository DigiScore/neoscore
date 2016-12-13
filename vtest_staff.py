#!/usr/bin/env python3

from brown.core import brown
from brown.utils.units import Mm, StaffUnit
from brown.core.flowable_frame import FlowableFrame
from brown.primitives.staff import Staff
from brown.primitives.clef import Clef


brown.setup()

# Test hacky use of flowable coordinate space
flow = FlowableFrame((Mm(0), Mm(0)), Mm(35000), Mm(20), Mm(20))
staff = Staff((Mm(0), Mm(0)), Mm(2000), flow, Mm(1))
staff.render()

clef = Clef(staff, Mm(5), 'treble')
clef.render()

brown.show()
