import pytest

from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import Mm
from neoscore.western.pedal_line import PedalLine
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestPedalLine(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(ORIGIN, None, Mm(100))

    def test_full_pedal_line(self):
        pedal_line = PedalLine(ORIGIN, self.staff, Mm(100))
        assert pedal_line.pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert pedal_line.end_pos == Point(x=Mm(100.0), y=Mm(0.0))
        assert pedal_line.elements[0].pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert pedal_line.elements[3].pos == Point(x=Mm(100.0), y=Mm(0.0))

    def test_pedal_line_half_lift(self):
        pedal_line = PedalLine(
            ORIGIN, self.staff, Mm(100), half_lift_positions=[Mm(10), Mm(50), Mm(95)]
        )
        assert pedal_line.elements[3].pos == Point(x=Mm(10.0), y=Mm(0.0))
        assert pedal_line.elements[6].pos == Point(x=Mm(50.0), y=Mm(0.0))
        assert pedal_line.elements[9].pos == Point(x=Mm(95.0), y=Mm(0.0))

    def test_pedal_line_half_lift_too_long(self):
        with pytest.raises(AttributeError):
            PedalLine(
                ORIGIN,
                self.staff,
                Mm(100),
                half_lift_positions=[Mm(10), Mm(50), Mm(120)],
            )
