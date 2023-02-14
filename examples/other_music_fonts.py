from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.repeating_music_text_line import RepeatingMusicTextLine
from neoscore.core.units import ZERO, Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.key_signature import KeySignature
from neoscore.western.staff import Staff
from neoscore.western.time_signature import TimeSignature

neoscore.setup()

# To run, set these to the path of a downloaded SMuFL-compliant font like Sebastian
# https://github.com/fkretlow/sebastian
#
# e.g. /path/to/Sebastian.otf
FONT_FILE_PATH = ""
# e.g. /path/to/Sebastian.json
METADATA_PATH = ""
# e.g. "Sebastian"
FONT_FAMILY_NAME = ""

neoscore.register_music_font(FONT_FILE_PATH, METADATA_PATH)

staff = Staff((Mm(40), Mm(30)), None, Mm(100), music_font_family="Sebastian")
Clef(ZERO, staff, "treble")
KeySignature(ZERO, staff, "b_major")
TimeSignature(ZERO, staff, (10, 16))
Chordrest(ZERO, staff, ["f", "a", "b", "dn"], (3, 32))
RepeatingMusicTextLine(
    (ZERO, Mm(-3)),
    staff,
    (Mm(15), ZERO),
    None,
    "ornamentZigZagLineWithRightEnd",
    "ornamentTrill",
)

render_example("other_music_fonts")
