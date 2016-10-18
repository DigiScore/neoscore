#!/usr/bin/env python3

from brown.core import brown
from brown.core.text_object import TextObject
from brown.core.glyph import Glyph
from brown.core.path import Path


brown.setup()

# text = TextObject(0, 300, 'hello')
# text.draw()
# text_2 = TextObject(0, 0, 'world')
# text_2.draw()

# glyph = Glyph(100, 100, 'o')
# glyph.draw()

path = Path(0, 0)

path.line_to(30, 40)
path.cubic_to(30, 40, 90, 60, 100, 100)
path.cubic_to(80, 80, 10, 120, 50, 75)
path.render()

line = Path.straight_line(50, 50, 50, 50)
line.render()


brown.show()
