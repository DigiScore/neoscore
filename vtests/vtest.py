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
from brown.primitives.repeating_music_text_line import RepeatingMusicTextLine


brown.setup()

# Test hacky use of flowable coordinate space
flow = FlowableFrame((Mm(0), Mm(0)), Mm(35000), Mm(30), Mm(10))

staff = Staff((Mm(0), Mm(0)), Mm(2000), flow, Mm(1))

lower_staff = Staff((Mm(0), Mm(9)), Mm(2000), flow, Mm(1))

lowest_staff = Staff((Mm(10), Mm(18)), Mm(2000), flow, Mm(1))

barline = BarLine(Mm(30), [staff, lower_staff, lowest_staff])

staff.add_clef((0, 4), 'treble')
lower_staff.add_clef((0, 4), 'treble')
staff.add_time_signature(0, (4, 4))
staff.add_chordrest((1, 4), ["a'", "bs"], (2, 4))

font = Font('Cormorant Garamond', Mm(2), weight=100, italic=True)

regular_text = TextObject((Mm(20), staff.unit(-1)),
                          'piu mosso',
                          font=font,
                          parent=staff)

p = Dynamic((Mm(20), staff.unit(6)), 'p', staff)

sfz = Dynamic.sfz((Mm(25), staff.unit(6)), staff)

hairpin = Hairpin((Mm(0), Mm(3), 0, p), (Mm(0), Mm(3), 0, sfz), 1)

slur = Slur((Mm(0), Mm(0), 0, regular_text),
            (Mm(0), Mm(0), 0, sfz))

brace = Brace(Mm(0), Mm(500), {staff, lower_staff, lowest_staff})

import random
random_wiggles = [random.choice(['wiggleRandom1',
                                 'wiggleRandom2',
                                 'wiggleRandom3',
                                 'wiggleRandom4']) for i in range(100)]

MusicTextObject((Mm(25), staff.unit(2)),
                random_wiggles,
                staff)

for i in range(0, 50, 2):
    factor = 1 + (i / 10)
    MusicTextObject((Mm(10 + i), lowest_staff.unit(4)),
                    ['brace', ('gClef', 1)],
                    lowest_staff,
                    scale_factor=factor)

print('rendering flowing_text')
flowing_text = MusicTextObject((Mm(155), lower_staff.unit(3)),
                               ['gClef'] * 130,
                               lower_staff,
                               scale_factor=1)

pen = Pen(thickness=Mm(0.2), pattern=5)
explicit_path = Path((Mm(0), Mm(0)), pen, parent=p)
explicit_path.line_to(Mm(500), Mm(20))

fake_trill = RepeatingMusicTextLine((Mm(30), staff.unit(-6), 0, staff),
                                    (Mm(500), staff.unit(-6), 0, staff),
                                    'wiggleTrill')

text_on_first_page = TextObject((Mm(0), Mm(0), 0),
                                 'first page!')

text_on_second_page = TextObject((Mm(0), Mm(0), 1),
                                 'second page!')

text_on_third_page = TextObject((Mm(0), Mm(0), 1),
                                'third page!',
                                parent=text_on_second_page)

explicit_path_on_third_page = Path((Mm(0), Mm(0), 1), parent=text_on_second_page)
explicit_path_on_third_page.line_to(Mm(100), Mm(60))

brown.show()
