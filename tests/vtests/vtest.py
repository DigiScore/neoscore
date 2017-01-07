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


brown.setup()

# Test hacky use of flowable coordinate space
flow = FlowableFrame((Mm(0), Mm(0)), Mm(35000), Mm(20), Mm(10))
flow.render()

staff = Staff((Mm(0), Mm(0)), Mm(2000), flow, Mm(1))
staff.render()

glyph = MusicGlyph((staff.unit(10), staff.unit(0.5)), 'noteheadBlack', parent=staff)
glyph.render()

treble_clef = Clef(staff, Mm(0), 'treble')
treble_clef.render()

chord = ChordRest(Mm(20), staff, ["c'", "as'", "fn'''", "gf"])
chord.render()

simple_path = Path((Mm(0), Mm(0)), parent=treble_clef)
simple_path.line_to(Mm(10), Mm(-10))
simple_path.line_to(Mm(10), Mm(0))
simple_path.render()

path = Path((Mm(0), Mm(0)), parent=glyph)
path.line_to(Mm(3), Mm(-10))
path.line_to(AnchoredPoint(Mm(1), Mm(0), chord))
path.render()
import pdb; pdb.set_trace()

brown.show()
