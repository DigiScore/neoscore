#!/usr/bin/env python3

from brown.core import brown
from brown.core.text_object import TextObject
from brown.core.glyph import Glyph


brown.setup()

text = TextObject(0, 300, 'hello')
text.draw()
text_2 = TextObject(0, 0, 'world')
text_2.draw()

glyph = Glyph(100, 100, 'o')
glyph.draw()


brown.show()
