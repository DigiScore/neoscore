from neoscore.core.units import Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.duration import Duration
from neoscore.western.key_signature import KeySignature
from neoscore.western.staff import Staff

from ..helpers import AppTest, render_scene


class TestStaffOutsideFlowable(AppTest):
    def test_staff_with_notes(self):
        staff = Staff((Mm(0), Mm(0)), None, Mm(100), line_spacing=Mm(1))

        unit = staff.unit
        clef = Clef(unit(0), staff, "treble")
        KeySignature(clef.bounding_rect.width + unit(0.5), staff, "g_major")

        Chordrest(unit(8), staff, ["g''"], Duration(1, 8))
        Chordrest(unit(10), staff, [], Duration(1, 4))

        render_scene()
