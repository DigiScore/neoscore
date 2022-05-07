from helpers import render_example

from neoscore.common import *
from neoscore.core import paper

neoscore.setup(paper=paper.LETTER)


# This line should exactly span the complete page width
Path.straight_line((Inch(-1), Inch(2)), None, (Inch(8.5), Inch(0)))


# This text should almost exactly span the page live width
size_12_pt_text = Text((Mm(00), Mm(10)), None, "SIZE 12 " * 11, Font("Lora", Unit(12)))

# These two lines should be the same height, and should be just a bit taller than the text
Path.straight_line((Mm(-2), ZERO), size_12_pt_text, (ZERO, Unit(-12)))
Path.straight_line((Mm(-4), ZERO), size_12_pt_text, (ZERO, Mm(-4.2333)))

render_example("measurements")
