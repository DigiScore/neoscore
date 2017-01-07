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

chord_1 = ChordRest(Mm(20), staff, ["c'", "as'", "fn'''", "gf"])
chord_1.render()

chord_2 = ChordRest(Mm(40), staff, ["b'", "as'", "fn''", "gf"])
chord_2.render()

path = Path((Mm(0), Mm(0)), parent=glyph)
path.line_to(Mm(3), Mm(-10))
path.line_to(AnchoredPoint(Mm(1), Mm(0), chord_1))
path.render()

slur = Slur(chord_1, chord_2)
slur.render()

brown.show()
