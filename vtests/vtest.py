#!/usr/bin/env python3

from brown.core import brown
from brown.utils.anchored_point import AnchoredPoint
from brown.utils.units import Mm, GraphicUnit
from brown.core.flowable_frame import FlowableFrame
from brown.core.font import Font
from brown.primitives.staff import Staff
from brown.primitives.clef import Clef
from brown.primitives.chordrest import ChordRest
from brown.utils.point import Point
from brown.core.music_text_object import MusicTextObject
from brown.core.path import Path
from brown.primitives.slur import Slur
from brown.core.pen import Pen
from brown.core.text_object import TextObject
from brown.utils.color import Color
from brown.primitives.time_signature import TimeSignature
from brown.primitives.bar_line import BarLine
from brown.primitives.rest import Rest
from brown.primitives.beam import Beam
from brown.primitives.rhythm_dot import RhythmDot
from brown.primitives.brace import Brace
from brown.primitives.dynamic import Dynamic
from brown.primitives.hairpin import Hairpin


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

font = Font('Cormorant Garamond', Mm(2), weight=100, italic=True)

regular_text = TextObject((Mm(20), staff.unit(-1)),
                          'piu mosso',
                          font=font,
                          parent=staff)
regular_text.render()

p = Dynamic((Mm(20), staff.unit(6)), 'p', staff)
p.render()

sfz = Dynamic.sfz((Mm(25), staff.unit(6)), staff)
sfz.render()

hairpin = Hairpin((Mm(0), Mm(3), p), (Mm(0), Mm(3), sfz), 1)
hairpin.render()

slur = Slur((Mm(0), Mm(0), regular_text),
            (Mm(0), Mm(0), sfz))
slur.render()

brace = Brace(Mm(0), Mm(500), {staff, lower_staff, lowest_staff})
brace.render()

MusicTextObject((Mm(25), lower_staff.unit(4)),
                ('brace', 4),
                lower_staff).render()

for i in range(0, 11):
    factor = 1 + (i / 10)
    MusicTextObject((Mm(10 + i), lowest_staff.unit(4)),
                    ['brace', ('gClef', 1)],
                    lowest_staff,
                    scale_factor=factor).render()

pen = Pen(pattern=3)
explicit_path = Path((Mm(3), Mm(-4)), pen, parent=p)
explicit_path.line_to(Mm(30), Mm(4))
explicit_path.render()

brown.show()
