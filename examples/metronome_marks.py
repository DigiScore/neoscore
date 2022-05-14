from helpers import render_example

from neoscore.common import *

neoscore.setup()

next_y = ZERO


def next_pos():
    global next_y
    val = (ZERO, next_y)
    next_y += Mm(20)
    return val


mfont = MusicFont("Bravura", Mm(1.5))


MetronomeMark(next_pos(), None, "metNoteQuarterUp", "= 60", mfont)

# Down-pointing noteheads are supported, but they aren't aligned nicely
MetronomeMark(next_pos(), None, "metNote8thDown", "= 120", mfont)

# This uses a unicode emdash, but you can use plain dashes too
MetronomeMark(next_pos(), None, "metNoteHalfUp", "= 80—100", mfont)

# The music text portion can contain multiple glyphs, just like `MusicText`.
# This is especially useful for writing rhythm dots
MetronomeMark(
    next_pos(),
    None,
    ["metNoteQuarterUp", "metAugmentationDot"],
    "= 120",
    mfont,
)

# Approx equal signs can be written using plain old unicode
MetronomeMark(next_pos(), None, "metNoteHalfUp", "≈ 116", mfont)

MetronomeMark(next_pos(), None, "metNoteHalfUp", "= 60, rubato", mfont)

# You can even use beamed groups
# See https://w3c.github.io/smufl/latest/tables/beamed-groups-of-notes.html
MetronomeMark(
    next_pos(),
    None,
    [
        "textBlackNoteShortStem",
        "textCont8thBeamShortStem",
        "textBlackNoteFrac8thShortStem",
        "textCont8thBeamShortStem",
        "textBlackNoteFrac8thShortStem",
    ],
    "= 120",
    mfont,
    spaces_between_music_chars=False,
)

render_example("doc-testing")
