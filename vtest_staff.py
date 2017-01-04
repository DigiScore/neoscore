#!/usr/bin/env python3

from brown.core import brown
from brown.utils.units import Mm
from brown.core.flowable_frame import FlowableFrame
from brown.primitives.staff import Staff
from brown.primitives.clef import Clef
from brown.core.glyph import Glyph
from brown.core.path import Path


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

clef = Clef(staff, Mm(0), 'treble')
from pprint import pprint; pprint(clef.glyph_info)
clef.render()

clef_bbox = clef._bounding_rect
path = Path(flow._map_to_doc(clef.pos))
path.line_to((clef_bbox.width, Mm(0)))
path.line_to((clef_bbox.width, clef_bbox.height))
path.render()


# for i in range(100):
#     Clef(staff, Mm(i*5), 'treble').render()

brown.show()
