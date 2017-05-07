import unittest

import pytest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.paper import Paper
from brown.core.staff import Staff, NoClefError
from brown.core.clef import Clef
from brown.core.octave_line import OctaveLine
from brown.models.clef_type import ClefType
from brown.utils.point import Point
from brown.utils.units import Mm


class TestStaff(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_height(self):
        # 5 lines
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100),
                  self.flowable, staff_unit=Mm(1.5), line_count=5).height,
            Mm(6))
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100),
                  self.flowable, staff_unit=Mm(1), line_count=5).height,
            Mm(4))
        # 4 lines
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100),
                  self.flowable, staff_unit=Mm(1.5), line_count=4).height,
            Mm(4.5))
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100),
                  self.flowable, staff_unit=Mm(1), line_count=4).height,
            Mm(3))

    def test_distance_to_next_of_type(self):
        staff = Staff((Mm(10), Mm(0)), Mm(100), self.flowable)
        treble = Clef(staff, Mm(11), 'treble')
        bass = Clef(staff, Mm(31), 'bass')
        staff.distance_to_next_of_type(treble)._assert_almost_equal(Mm(20))
        staff.distance_to_next_of_type(bass)._assert_almost_equal(Mm(100 - 31))

    def test_active_clef_at_with_explicit_clefs(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable)
        Clef(staff, Mm(0), 'treble')
        Clef(staff, Mm(10), 'bass')
        # Test between two clefs should have treble in effect
        assert(staff.active_clef_at(Mm(1)).clef_type == ClefType.treble)
        # Test after bass clef goes into effect
        assert(staff.active_clef_at(Mm(11)).clef_type == ClefType.bass)

    def test_active_clef_at_with_implicit_default_clef(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable)
        assert(staff.active_clef_at(Mm(5)) is None)

    def test_active_transposition_at_with_octave_line_with_staff_parent(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable)
        octave_line = OctaveLine((Mm(20), Mm(0)), staff, Mm(80),
                                 indication='8va')
        assert(staff.active_transposition_at(Mm(0)) is None)
        assert(staff.active_transposition_at(Mm(20))
               == octave_line.transposition)
        assert(staff.active_transposition_at(Mm(100))
               == octave_line.transposition)
        assert(staff.active_transposition_at(Mm(101)) is None)

    def test_middle_c_at_with_explicit_clefs(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable)
        Clef(staff, Mm(0), 'treble')
        Clef(staff, Mm(10), 'bass')
        # Test between two clefs should be in treble mode
        assert(staff.middle_c_at(Mm(1)) == staff.unit(5))
        # Test after bass clef goes into effect
        assert(staff.middle_c_at(Mm(11)) == staff.unit(-1))

    def test_middle_c_at_with_implicit_default_clef(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable)
        with pytest.raises(NoClefError):
            staff.middle_c_at(Mm(5))

    def test_middle_c_at_with_active_octave_line(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable)
        Clef(staff, Mm(0), 'treble')
        octave_line = OctaveLine((Mm(20), Mm(0)), staff, Mm(80),
                                 indication='8va')
        # Before octave_line goes into effect
        assert(staff.middle_c_at(Mm(0)) == staff.unit(5))
        # While octave_line is in effect
        assert(staff.middle_c_at(Mm(20)) == staff.unit(8.5))
        assert(staff.middle_c_at(Mm(100)) == staff.unit(8.5))
        # After octave_line ends
        assert(staff.middle_c_at(Mm(101)) == staff.unit(5))

    def test_position_outside_staff_is_inverse_of_inside(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable, line_count=4)
        i = -1
        while i < 5:
            assert(staff.y_outside_staff(staff.unit(i)) !=
                   staff.y_inside_staff(staff.unit(i)))
            i += 1

    def test_position_inside_staff_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable, line_count=5)
        assert(staff.y_inside_staff(staff.unit(0)) is True)
        assert(staff.y_inside_staff(staff.unit(4)) is True)
        assert(staff.y_inside_staff(staff.unit(5)) is False)
        assert(staff.y_inside_staff(staff.unit(-5)) is False)

    def test_position_inside_staff_with_even_line_count(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable, line_count=4)
        assert(staff.y_inside_staff(staff.unit(0)) is True)
        assert(staff.y_inside_staff(staff.unit(3)) is True)
        assert(staff.y_inside_staff(staff.unit(4)) is False)
        assert(staff.y_inside_staff(staff.unit(-4)) is False)

    def test_position_on_ledger_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable, line_count=5)
        assert(staff.y_on_ledger(staff.unit(-1)) is True)
        assert(staff.y_on_ledger(staff.unit(-0.5)) is False)
        assert(staff.y_on_ledger(staff.unit(0)) is False)
        assert(staff.y_on_ledger(staff.unit(4)) is False)
        assert(staff.y_on_ledger(staff.unit(4.5)) is False)
        assert(staff.y_on_ledger(staff.unit(5)) is True)

    def test_ledgers_needed_from_position_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.flowable, line_count=5)
        # Inside the staff, no ledgers
        assert(staff.ledgers_needed_for_y(staff.unit(0)) == set())
        assert(staff.ledgers_needed_for_y(staff.unit(4)) == set())
        # Just outside the staff, no ledgers
        assert(staff.ledgers_needed_for_y(staff.unit(-0.5)) == set())
        assert(staff.ledgers_needed_for_y(staff.unit(4.5)) == set())
        # Right on the first ledger
        assert(staff.ledgers_needed_for_y(staff.unit(-1)) ==
               {staff.unit(-1)})
        assert(staff.ledgers_needed_for_y(staff.unit(5)) ==
               {staff.unit(5)})
        # Further outside with multiple ledgers, directly on lines
        assert(staff.ledgers_needed_for_y(staff.unit(6)) ==
               {staff.unit(6), staff.unit(5)})
        assert(staff.ledgers_needed_for_y(staff.unit(-2)) ==
               {staff.unit(-2), staff.unit(-1)})
        # Further outside with multiple ledgers, between lines
        assert(staff.ledgers_needed_for_y(staff.unit(6.5)) ==
               {staff.unit(6), staff.unit(5)})
        assert(staff.ledgers_needed_for_y(staff.unit(-2.5)) ==
               {staff.unit(-2), staff.unit(-1)})

    def test_elements_when_not_located_at_origin(self):
        """Regression test

        Ensure lines are drawn at the correct locations when staff is not
        positioned at (0, 0)
        """
        staff = Staff((Mm(2), Mm(3)), Mm(10),
                      self.flowable, staff_unit=Mm(1), line_count=5)
        staff.render()
        # Top line
        assert(staff.elements[0].pos == Point(Mm(0), Mm(0)))
        assert(staff.elements[0].parent == staff)
        assert(staff.elements[1].pos == Point(Mm(10), Mm(0)))
        assert(staff.elements[1].parent == staff)
        # Second line
        assert(staff.elements[2].pos == Point(Mm(0), Mm(1)))
        assert(staff.elements[2].parent == staff)
        assert(staff.elements[3].pos == Point(Mm(10), Mm(1)))
        assert(staff.elements[3].parent == staff)
