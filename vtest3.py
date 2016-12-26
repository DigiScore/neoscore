#!/usr/bin/env python3

import random

from brown.core import brown
from brown.core.glyph import Glyph
from brown.core.flowable_frame import FlowableFrame
from brown.core.path import Path
from brown.utils.units import Mm

from brown.config import config


brown.setup()

flow = FlowableFrame((Mm(20), Mm(0)), Mm(3500), Mm(20))
flow.render()
# Test flowable paths
path = Path((Mm(30), Mm(1)), parent=flow)
for i in range(200):
    path.line_to((Mm(i * 10), Mm(random.randint(0, 19))))
path.render()


brown.show()
