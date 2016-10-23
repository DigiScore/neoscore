#!/usr/bin/env python3

from brown.utils import units
from brown.core import brown
from brown.core.font import Font
from brown.core.text_object import TextObject
from brown.core.glyph import Glyph
from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.brush import Brush
from brown.primitives.staff import Staff
from brown.primitives.notehead import Notehead
from brown.config import config


brown.setup()


path = Path(0, 0, Pen('#f29000'), Brush('#eeeeee'))
path.line_to(30, 40)
path.cubic_to(30, 40, 90, 60, 100, 100)
path.cubic_to(80, 80, 10, 120, 50, 75)
path.close_subpath()
path.render()

glyph = Glyph(50, 00, '\uE118', brown.music_font)
glyph.render()

line = Path.straight_line(50, 50, 50, 50)
line.render()

text = TextObject(120, 10, 'hello')
text.brush = Brush('#00ffff')
text.render()

staff = Staff(30, 0, 200, 1)
staff.render()

pitches = ["d'", "e'", "f'", "g'", "a'", "b'",
           "c''", "d''", "e''", "f''"]
for i, pitch in enumerate(pitches):
    Notehead(staff, i * 20, pitch).render()


brown.show()
