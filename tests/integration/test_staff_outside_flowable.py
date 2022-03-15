import tempfile

from neoscore.common import *


def test_staff_with_notes():
    neoscore.setup()

    staff = Staff((Mm(0), Mm(0)), None, Mm(100), Mm(1))

    unit = staff.unit
    clef = Clef(unit(0), staff, "treble")
    KeySignature(clef.bounding_rect.width + unit(0.5), staff, "g_major")

    Chordrest(unit(8), staff, ["g''"], Beat(1, 8))
    Chordrest(unit(10), staff, [], Beat(1, 4))

    out_file = tempfile.NamedTemporaryFile(suffix=".png")
    neoscore.render_image((Mm(-100), Mm(-100), Mm(100), Mm(100)), out_file.name)
