#!/usr/bin/env python3

from brown.core import brown
from brown.core.text_object import TextObject
from brown.core.glyph import Glyph
from brown.core.path import Path


brown.setup()

path = Path(0, 0)

path.line_to(30, 40)
path.cubic_to(30, 40, 90, 60, 100, 100)
path.cubic_to(80, 80, 10, 120, 50, 75)
path.render()

line = Path.straight_line(50, 50, 50, 50)
line.render()

text = TextObject(80, 10, 'hello')
text.render()

brown.show()
