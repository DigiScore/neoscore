#!/usr/bin/env python3

from brown.utils import units
from brown.core import brown
from brown.core.font import Font
from brown.core.text_object import TextObject
from brown.core.glyph import Glyph
from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.brush import Brush
from brown.primitives.clef import Clef
from brown.primitives.staff import Staff
from brown.primitives.notehead import Notehead
from brown.primitives.chordrest import ChordRest
from brown.primitives.ledger_line import LedgerLine

from brown.config import config


brown.setup()


path = Path(0, 0, Pen('#f29000'), Brush('#eeeeee'))
path.line_to(30, 40)
path.cubic_to(30, 40, 90, 60, 100, 100)
path.cubic_to(80, 80, 10, 120, 50, 75)
path.close_subpath()
path.render()

glyph = Glyph(50, 100, '\uE118', brown.music_font)
glyph.render()

line = Path.straight_line(50, 50, 50, 50)
line.render()

Path.straight_line(0, 0, 200, 200).render()


text = TextObject(120, 10, 'hello')
text.brush = Brush('#00ffff')
text.render()

staff = Staff(0, 0, 300, 1)
staff.render()

clef = Clef(staff, 0, 'alto')
clef.render()

clef = Clef(staff, 150, 'treble')
clef.render()

pitches = ["d'", "e'", "f'", "g'", "a'", "b'",
           "c''", "d''", "e''", "f''"]
for i, pitch in enumerate(pitches):
    Notehead(staff, i * 20 + 30, pitch).render()

Notehead(staff, 0, "c'").render()

# dummy ledgers
ledger = LedgerLine(staff, 97, 6)
ledger.render()

# chordrest
chord_pitches = ["c'", "e'", "g'", "a'"]
chordrest = ChordRest(staff, chord_pitches, 270)
chordrest.render()

# one note chordrest high above the staff
ChordRest(staff, ["d''''"], 220).render()

# Draw vertical line at chordrest 0 position
# Path.straight_line(270, 0, 0, 100).render()


brown.show()
