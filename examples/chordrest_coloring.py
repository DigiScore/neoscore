from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.color import ColorDef
from neoscore.core.directions import DirectionY
from neoscore.core.pen import Pen
from neoscore.core.rich_text import RichText
from neoscore.core.units import ZERO, Mm
from neoscore.western.beam_group import BeamGroup
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff

neoscore.setup()


annotation_1 = """
The Chordrest container does not have built-in support for overriding the colors of
noteheads and other component objects (accidentals, stems, flags, etc.), but we can
change the colors by accessing the component objects after init.
"""
RichText((Mm(1), Mm(1)), None, annotation_1, width=Mm(120))

staff_1 = Staff((Mm(10), Mm(30)), None, Mm(100))
Clef(ZERO, staff_1, "treble")
c1 = Chordrest(ZERO, staff_1, ["c"], (1, 8))
c1.noteheads[0].brush = Brush("#ff0000")

# Noteheads are indexed by the same order as specified in the given pitch list.
c2 = Chordrest(Mm(15), staff_1, ["eb", "g", "bb", "c'"], (1, 16))
c2.noteheads[0].brush = Brush("#ff0000")
c2.noteheads[2].brush = Brush("#00ff00")

c3 = Chordrest(Mm(25), staff_1, ["en'"], (1, 32))
c3.flag.brush = Brush("#0000ff")
c3.stem.brush = Brush("#0000ff")


# Changing the brushes of *all* component objects is a bit tedious.
# You can use this snippet to accomplish that.
# We may upstream something like this later on.
def change_all_chordrest_colors(cr: Chordrest, color: ColorDef):
    """Change the colors of all Chordrest component objects.

    This does not change any attached beams.
    """
    brush = Brush(color)
    for notehead in cr.noteheads:
        notehead.brush = Brush.from_existing(notehead.brush, color)
    for accidental in cr.accidentals:
        accidental.brush = Brush.from_existing(accidental.brush, color)
    for ledger in cr.ledgers:
        ledger.pen = Pen.from_existing(ledger.pen, color=color)
    for dot in cr.dots:
        dot.brush = Brush.from_existing(ledger.brush, color)
    if cr.stem:
        cr.stem.pen = Pen.from_existing(cr.stem.pen, color=color)
    if cr.flag:
        cr.flag.brush = Brush.from_existing(cr.flag.brush, color)
    if cr.rest:
        cr.rest.brush = Brush.from_existing(cr.rest.brush, color)


c4 = Chordrest(Mm(35), staff_1, ["en'", "bn'"], (3, 32))
change_all_chordrest_colors(c4, "#ff00ff")

c5 = Chordrest(Mm(50), staff_1, ["c''"], (1, 16))
c6 = Chordrest(Mm(60), staff_1, ["g'"], (1, 16))
# Notice how the beams are colored separately.
BeamGroup([c5, c6], brush="#ff0000", pen="#ff0000")
change_all_chordrest_colors(c5, "00ff00")
change_all_chordrest_colors(c6, "0000ff")


annotation_2 = """
The main limitation of this approach is that these overrides are lost whenever the chord
is rebuilt. Rebuilds are triggered whenever higher-level Chordrest properties are
changed which affect the chord's contents, for example flipping the stem direction or
changing notes. Rebuilds can also be triggered when attaching a BeamGroup to
chords. Here, a chord's overridden colors are reset by a subsequent stem direction
override.
"""
RichText((Mm(1), Mm(60)), None, annotation_2, width=Mm(120))

staff_2 = Staff((Mm(10), Mm(110)), None, Mm(100))
Clef(ZERO, staff_2, "treble")

c7 = Chordrest(ZERO, staff_2, ["c"], (1, 8))
change_all_chordrest_colors(c7, "#ff0000")
c7.stem_direction = DirectionY.DOWN


render_example("chordrest_coloring")
