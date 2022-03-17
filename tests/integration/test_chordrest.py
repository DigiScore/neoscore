import tempfile

from neoscore.common import *


def test_chordrest():
    neoscore.setup()

    staff = Staff((Mm(0), Mm(0)), None, Mm(100), Mm(1))

    unit = staff.unit
    clef = Clef(unit(0), staff, "treble")
    KeySignature(clef.bounding_rect.width + unit(0.5), staff, "g_major")

    # Chord with ledgers, dots, flags, and accidentals
    Chordrest(unit(8), staff, ["gs'''", "cf'", "a,,,"], Beat(3, 64))

    # Rest with dots
    Chordrest(unit(20), staff, None, Beat(7, 128))

    out_file = tempfile.NamedTemporaryFile(suffix=".png")
    neoscore.render_image((Mm(-100), Mm(-100), Mm(100), Mm(100)), out_file.name)
