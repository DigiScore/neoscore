#!/usr/bin/env python3

import random

from brown.core import brown
from brown.core.glyph import Glyph
from brown.core.flowable_frame import FlowableFrame
from brown.core.path import Path
from brown.utils.units import Mm
from brown.utils.point import Point

from brown.config import config


brown.setup()

flow = FlowableFrame((Mm(0), Mm(0)), Mm(3500), Mm(20))
flow.render()
# Test flowable paths
path = Path((Mm(30), Mm(1)), parent=flow)
path.line_to((Mm(150), Mm(20)))
path._render_slice(Point(Mm(50), Mm(21)), 0, Mm(130))
#path._render_slice(Point(Mm(40), 0), 30, 30)
#for i in range(3):
#    path.line_to((Mm(i * 10), Mm(random.randint(0, 19))))
path.render()


brown.show()
