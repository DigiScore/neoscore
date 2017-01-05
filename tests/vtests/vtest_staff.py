#!/usr/bin/env python3

from brown.core import brown
from brown.utils.units import Mm, GraphicUnit
from brown.core.flowable_frame import FlowableFrame
from brown.primitives.staff import Staff
from brown.primitives.clef import Clef
from brown.primitives.chordrest import ChordRest
from brown.utils.point import Point
from brown.core.glyph import Glyph
from brown.core.music_glyph import MusicGlyph
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

glyph = MusicGlyph((staff.unit(10), staff.unit(0.5)), 'noteheadBlack', parent=staff)
glyph.render()

treble_clef = Clef(staff, Mm(0), 'treble')
treble_clef.render()

chord = ChordRest(Mm(20), staff, ["c'", "a'"])
chord.render()

path = Path((Mm(0), Mm(0)), parent=glyph)
path.line_to((Mm(10), Mm(3)))
path.render()

brown.show()
