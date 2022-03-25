from neoscore.core import neoscore
from neoscore.models.beat import Beat
from neoscore.utils.units import Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.key_signature import KeySignature
from neoscore.western.staff import Staff
from tests.helpers import render_scene


def test_staff_with_notes():
    neoscore.setup()

    staff = Staff((Mm(0), Mm(0)), None, Mm(100), Mm(1))

    unit = staff.unit
    clef = Clef(unit(0), staff, "treble")
    KeySignature(clef.bounding_rect.width + unit(0.5), staff, "g_major")

    Chordrest(unit(8), staff, ["g''"], Beat(1, 8))
    Chordrest(unit(10), staff, [], Beat(1, 4))

    render_scene()
