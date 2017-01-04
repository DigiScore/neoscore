#!/usr/bin/env python3

import random

from brown.utils.units import Mm
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
from brown.core.flowable_frame import FlowableFrame
from brown.utils.units import GraphicUnit

from brown.config import config


brown.setup()

glyph = Glyph((50, 100), '\uE0A4', brown.music_font)
glyph.render()
new_y = GraphicUnit(100) + (glyph.font.em_size / 4)
glyph2 = Glyph((50, new_y), '\uE0A4', brown.music_font)
glyph2.render()

path = Path((0, 0), Pen('#000000'), Brush('#eeeeee'))
#path.line_to((25, 25))
#path.line_to((25, 50))
#path.line_to((0, 50))
path.line_to(0, 0, glyph)
path.render()

curve = Path((0, 0), Pen('#000000'), Brush('#eeeeee'))
curve.cubic_to((0, 50, glyph), (50, 0, glyph), (0, -50, glyph))
curve.render()



brown.show()
