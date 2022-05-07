from neoscore.core import neoscore
from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm
from neoscore.western.instrument_name import InstrumentName
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestInstrumentName(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(ORIGIN, None, Mm(100))

    def test_default_font(self):
        obj = InstrumentName(ORIGIN, self.staff, "foo")
        assert obj.font == neoscore.default_font

    def test_font_override(self):
        font = neoscore.default_font.modified(size=Mm(10))
        obj = InstrumentName(ORIGIN, self.staff, "foo", font=font)
        assert obj.font == font

    def test_later_text_resolution(self):
        assert (
            InstrumentName(ORIGIN, self.staff, "foo")._resolved_later_lines_text
            == "foo"
        )
        assert (
            InstrumentName(ORIGIN, self.staff, "foo", "bar")._resolved_later_lines_text
            == "bar"
        )

    def test_breakable_length_is_full_staff(self):
        assert (
            InstrumentName(ORIGIN, self.staff, "foo").breakable_length
            == self.staff.breakable_length
        )

    def test_underlying_position_always_origin(self):
        assert InstrumentName((Mm(1), Mm(2)), self.staff, "foo").pos == ORIGIN
