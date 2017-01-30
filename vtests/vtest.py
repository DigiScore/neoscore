#!/usr/bin/env python3

from brown.core import brown
from brown.utils.anchored_point import AnchoredPoint
from brown.utils.units import Mm, GraphicUnit
from brown.core.flowable_frame import FlowableFrame
from brown.primitives.staff import Staff
from brown.primitives.clef import Clef
from brown.primitives.chordrest import ChordRest
from brown.utils.point import Point
from brown.core.glyph import Glyph
from brown.core.music_glyph import MusicGlyph
from brown.core.path import Path
from brown.primitives.slur import Slur
from brown.core.pen import Pen
from brown.utils.color import Color
from brown.primitives.time_signature import TimeSignature
from brown.primitives.bar_line import BarLine
from brown.primitives.rest import Rest
from brown.primitives.beam import Beam
from brown.primitives.rhythm_dot import RhythmDot


brown.setup()

# Test hacky use of flowable coordinate space
flow = FlowableFrame((Mm(0), Mm(0)), Mm(35000), Mm(30), Mm(10))
flow.render()

staff = Staff((Mm(0), Mm(0)), Mm(2000), flow, Mm(1))
staff.render()

lower_staff = Staff((Mm(0), Mm(9)), Mm(2000), flow, Mm(1))
lower_staff.render()

lowest_staff = Staff((Mm(10), Mm(18)), Mm(2000), flow, Mm(1))
lowest_staff.render()

barline = BarLine(Mm(30), [staff, lower_staff, lowest_staff])
barline.render()

staff.add_clef((0, 4), 'treble')
lower_staff.add_clef((0, 4), 'treble')
staff.add_time_signature(0, (4, 4))
staff.add_chordrest((1, 4), ["a'", "bs"], (2, 4))

for i in range(0, 11):
    factor = 1 + (i / 10)
    MusicGlyph((Mm(10 + i), lowest_staff.unit(4)),
               'brace', parent=lowest_staff, scale_factor=factor).render()

brown.show()
