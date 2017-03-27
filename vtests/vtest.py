#!/usr/bin/env python3

"""A development sandbox used for manually checking visual outputs."""

import os

from brown.common import *

brown.setup()

flow = FlowableFrame((Mm(0), Mm(0)), Mm(35000), Mm(30), Mm(10))

counting_string = '    '.join(str(x) for x in range(600))
counting_text = Text((Mm(0), Mm(0)), counting_string, parent=flow)
counting_text._breakable_width = Mm(10000)

staff = Staff((Mm(0), Mm(0)), Mm(10000), flow, Mm(1))

lower_staff = Staff((Mm(0), Mm(9)), Mm(7000), flow, Mm(1))

lowest_staff = Staff((Mm(10), Mm(18)), Mm(2000), flow, Mm(1))

barline = BarLine(Mm(30), [staff, lower_staff, lowest_staff])

upper_staff_clef = Clef(staff, Mm(0), 'treble')
lower_staff_clef = Clef(staff, Mm(0), 'treble')
upper_staff_time_signature = TimeSignature(Mm(0), Beat(4, 4), staff)

octave_line = OctaveLine((Mm(20), staff.unit(-2)), staff,
                         Mm(1000),
                         indication='8vb')


ChordRest(Mm(10), staff, ["a'", "bs"], Beat(2, 4))
ChordRest(Mm(40), staff, ["a'", "bs"], Beat(2, 4))
ChordRest(Mm(60), staff, ["b'", "bs"], Beat(2, 4))

font = Font('Cormorant Garamond', Mm(2), weight=100, italic=True)

regular_text = Text((Mm(20), staff.unit(-1)),
                    'piu mosso',
                    font=font,
                    parent=staff)

p = Dynamic((Mm(20), staff.unit(6)), 'p', staff)

sfz = Dynamic.sfz((Mm(25), staff.unit(6)), staff)

hairpin = Hairpin((Mm(0), Mm(3), p), (Mm(0), Mm(3), sfz), 1)

slur = Slur((Mm(0), Mm(0), regular_text),
            (Mm(0), Mm(0), sfz))

brace = Brace(Mm(0), Mm(5000), {staff, lower_staff, lowest_staff})

import random
random_wiggles = [random.choice(['wiggleRandom1',
                                 'wiggleRandom2',
                                 'wiggleRandom3',
                                 'wiggleRandom4']) for i in range(100)]

MusicText((Mm(25), staff.unit(2)),
          random_wiggles,
          staff)

scaling_texts = []
for i in range(0, 50, 2):
    factor = 1 + (i / 10)
    scaling_texts.append(
        MusicText((Mm(290 + i), lowest_staff.unit(4)),
                  ['brace', ('gClef', 1)],
                  lowest_staff,
                  scale_factor=factor))

flowing_text = MusicText((Mm(155), lower_staff.unit(3)),
                         ['gClef'] * 130,
                         lower_staff,
                         scale_factor=1)

pen = Pen(thickness=Mm(0.2), pattern=5)
explicit_path = Path((Mm(0), Mm(0)), pen, parent=p)
explicit_path.line_to(Mm(5000), Mm(100))

fake_trill = RepeatingMusicTextLine((Mm(30), staff.unit(-6), staff),
                                    (Mm(5000), staff.unit(-6), staff),
                                    'wiggleTrill')

text_on_first_page = Text((Mm(0), Mm(0)),
                          'first page!')

text_on_second_page = Text((Mm(0), Mm(0)),
                           'second page!',
                           parent=brown.document.pages[1])

text_on_third_page = Text((Mm(0), Mm(0)),
                          'third page!',
                          parent=brown.document.pages[2])

explicit_path_on_second_page = Path((Mm(0), Mm(0)), parent=text_on_second_page)
explicit_path_on_second_page.line_to(Mm(100), Mm(60))

ped_and_star_mark = PedAndStar((Mm(260), staff.unit(7)), staff, (Mm(30), staff.unit(0)))

# brown.show()

output_path = os.path.join(os.path.dirname(__file__), 'output', 'vtest_out.pdf')
brown.render_pdf(output_path)
print('Score exported to {}'.format(output_path))
