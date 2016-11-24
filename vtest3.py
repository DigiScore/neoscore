#!/usr/bin/env python3

import random

from brown.core import brown
from brown.core.glyph import Glyph
from brown.core.flowable_frame import FlowableFrame
from brown.utils.units import Mm
from tests.core.mock_flowable_object import MockFlowableObject

from brown.config import config


brown.setup()


# Test hacky use of flowable coordinate space
flow = FlowableFrame((Mm(20), Mm(0)), Mm(3500), Mm(20))
mock = MockFlowableObject((Mm(5), Mm(5)), Mm(3400), flow)
mock.render()


brown.show()
