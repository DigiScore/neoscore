import unittest

import pytest

from neoscore.core import neoscore
from neoscore.core.clef import Clef
from neoscore.core.flowable import Flowable
from neoscore.core.octave_line import OctaveLine
from neoscore.core.paper import Paper
from neoscore.core.staff import NoClefError, Staff
from neoscore.models.clef_type import ClefType
from neoscore.utils.point import Point
from neoscore.utils.units import Mm

from ..helpers import assert_almost_equal


class TestStaff(unittest.TestCase):
    def setUp(self):
        neoscore.setup(Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))

    def test_height(self):
        # 5 lines
        assert_almost_equal(
            Staff((Mm(0), Mm(0)), self.flowable, Mm(100), staff_unit=Mm(1.5), line_count=5).height,
            Mm(6),
        )
        assert_almost_equal(
            Staff((Mm(0), Mm(0)), self.flowable, Mm(100), staff_unit=Mm(1), line_count=5).height,
            Mm(4),
        )
        # 4 lines
        assert_almost_equal(
            Staff((Mm(0), Mm(0)), self.flowable, Mm(100), staff_unit=Mm(1.5), line_count=4).height,
            Mm(4.5),
        )
        assert_almost_equal(
            Staff((Mm(0), Mm(0)), self.flowable, Mm(100), staff_unit=Mm(1), line_count=4).height,
            Mm(3),
        )

    def test_distance_to_next_of_type(self):
        staff = Staff((Mm(10), Mm(0)), self.flowable, Mm(100))
        treble = Clef(Mm(11), staff, "treble")
        bass = Clef(Mm(31), staff, "bass")
        assert_almost_equal(staff.distance_to_next_of_type(treble), Mm(20))
        assert_almost_equal(staff.distance_to_next_of_type(bass), Mm(100 - 31))

    def test_active_clef_at_with_explicit_clefs(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        Clef(Mm(0), staff, "treble")
        Clef(Mm(10), staff, "bass")
        # Test between two clefs should have treble in effect
        assert staff.active_clef_at(Mm(1)).clef_type == ClefType.TREBLE
        # Test after bass clef goes into effect
        assert staff.active_clef_at(Mm(11)).clef_type == ClefType.BASS

    def test_active_clef_at_with_implicit_default_clef(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        assert staff.active_clef_at(Mm(5)) is None

    def test_active_transposition_at_with_octave_line_with_staff_parent(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        octave_line = OctaveLine((Mm(20), Mm(0)), staff, Mm(80), indication="8va")
        assert staff.active_transposition_at(Mm(0)) is None
        assert staff.active_transposition_at(Mm(20)) == octave_line.transposition
        assert staff.active_transposition_at(Mm(100)) == octave_line.transposition
        assert staff.active_transposition_at(Mm(101)) is None

    def test_middle_c_at_with_explicit_clefs(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        Clef(Mm(0), staff, "treble")
        Clef(Mm(10), staff, "bass")
        # Test between two clefs should be in treble mode
        assert staff.middle_c_at(Mm(1)) == staff.unit(5)
        # Test after bass clef goes into effect
        assert staff.middle_c_at(Mm(11)) == staff.unit(-1)

    def test_middle_c_at_with_implicit_default_clef(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        with pytest.raises(NoClefError):
            staff.middle_c_at(Mm(5))

    def test_middle_c_at_with_active_octave_line(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        Clef(Mm(0), staff, "treble")
        octave_line = OctaveLine((Mm(20), Mm(0)), staff, Mm(80), indication="8va")
        # Before octave_line goes into effect
        assert staff.middle_c_at(Mm(0)) == staff.unit(5)
        # While octave_line is in effect
        assert staff.middle_c_at(Mm(20)) == staff.unit(8.5)
        assert staff.middle_c_at(Mm(100)) == staff.unit(8.5)
        # After octave_line ends
        assert staff.middle_c_at(Mm(101)) == staff.unit(5)

    def test_position_inside_staff_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100), line_count=5)
        assert staff.y_inside_staff(staff.unit(0)) is True
        assert staff.y_inside_staff(staff.unit(4)) is True
        assert staff.y_inside_staff(staff.unit(5)) is False
        assert staff.y_inside_staff(staff.unit(-5)) is False

    def test_position_inside_staff_with_even_line_count(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100), line_count=4)
        assert staff.y_inside_staff(staff.unit(0)) is True
        assert staff.y_inside_staff(staff.unit(3)) is True
        assert staff.y_inside_staff(staff.unit(4)) is False
        assert staff.y_inside_staff(staff.unit(-4)) is False

    def test_position_on_ledger_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100), line_count=5)
        assert staff.y_on_ledger(staff.unit(-1)) is True
        assert staff.y_on_ledger(staff.unit(-0.5)) is False
        assert staff.y_on_ledger(staff.unit(0)) is False
        assert staff.y_on_ledger(staff.unit(4)) is False
        assert staff.y_on_ledger(staff.unit(4.5)) is False
        assert staff.y_on_ledger(staff.unit(5)) is True

    def test_ledgers_needed_from_position_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100), line_count=5)
        # Inside the staff, no ledgers
        assert staff.ledgers_needed_for_y(staff.unit(0)) == []
        assert staff.ledgers_needed_for_y(staff.unit(4)) == []
        # Just outside the staff, no ledgers
        assert staff.ledgers_needed_for_y(staff.unit(-0.5)) == []
        assert staff.ledgers_needed_for_y(staff.unit(4.5)) == []
        # Right on the first ledger
        assert staff.ledgers_needed_for_y(staff.unit(-1)) == [staff.unit(-1)]
        assert staff.ledgers_needed_for_y(staff.unit(5)) == [staff.unit(5)]
        # Further outside with multiple ledgers, directly on lines
        assert staff.ledgers_needed_for_y(staff.unit(6)) == [
            staff.unit(6),
            staff.unit(5),
        ]
        assert staff.ledgers_needed_for_y(staff.unit(-2)) == [
            staff.unit(-2),
            staff.unit(-1),
        ]
        # Further outside with multiple ledgers, between lines
        assert staff.ledgers_needed_for_y(staff.unit(6.5)) == [
            staff.unit(6),
            staff.unit(5),
        ]
        assert staff.ledgers_needed_for_y(staff.unit(-2.5)) == [
            staff.unit(-2),
            staff.unit(-1),
        ]

    def test_elements_when_not_located_at_origin(self):
        """Regression test

        Ensure lines are drawn at the correct locations when staff is not
        positioned at (0, 0)
        """
        staff = Staff((Mm(2), Mm(3)), self.flowable, Mm(10), staff_unit=Mm(1), line_count=5)
        staff._render()
        # Top line
        assert staff.elements[0].pos == Point(Mm(0), Mm(0))
        assert staff.elements[0].parent == staff
        assert staff.elements[1].pos == Point(Mm(10), Mm(0))
        assert staff.elements[1].parent == staff
        # Second line
        assert staff.elements[2].pos == Point(Mm(0), Mm(1))
        assert staff.elements[2].parent == staff
        assert staff.elements[3].pos == Point(Mm(10), Mm(1))
        assert staff.elements[3].parent == staff
