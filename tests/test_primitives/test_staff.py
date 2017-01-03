import unittest
from nose.tools import assert_raises

from brown.core import brown
from brown.utils.units import Mm
from brown.core.paper import Paper
from brown.core.flowable_frame import FlowableFrame
from brown.primitives.staff import Staff
from brown.primitives.clef import Clef


class TestStaff(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_staff_pos_to_top_down(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=5)
        # Center of staff
        assert(test_staff._staff_pos_to_top_down(0) == 4)
        # Above center
        assert(test_staff._staff_pos_to_top_down(1) == 3)
        assert(test_staff._staff_pos_to_top_down(4) == 0)
        assert(test_staff._staff_pos_to_top_down(5) == -1)
        assert(test_staff._staff_pos_to_top_down(12) == -8)
        # Below center
        assert(test_staff._staff_pos_to_top_down(-1) == 5)
        assert(test_staff._staff_pos_to_top_down(-4) == 8)
        assert(test_staff._staff_pos_to_top_down(-5) == 9)
        assert(test_staff._staff_pos_to_top_down(-12) == 16)

    def test_height(self):
        # 5 lines
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100), self.frame, staff_unit=1.5, line_count=5).height, 6)
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100), self.frame, staff_unit=1, line_count=5).height, 4)
        # 4 lines
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100), self.frame, staff_unit=1.5, line_count=4).height, 4.5)
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100), self.frame, staff_unit=1, line_count=4).height, 3)

    def test_active_clef_at_with_explicit_clefs(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        test_treble_clef = Clef(test_staff, 0,  'treble')
        test_bass_clef = Clef(test_staff, 10, 'bass')
        # Test between two clefs should have treble in effect
        assert(test_staff.active_clef_at(5) == test_treble_clef)
        # Test after bass clef goes into effect
        assert(test_staff.active_clef_at(15) == test_bass_clef)

    def test_active_clef_at_with_implicit_default_clef(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        # No clef specified - should default to None (implicit treble)
        assert(test_staff.active_clef_at(5) is None)

    def test_middle_c_at_with_explicit_clefs(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        test_treble_clef = Clef(test_staff, 0,  'treble')
        test_bass_clef = Clef(test_staff, 10, 'bass')
        # Test between two clefs should be in treble mode
        assert(test_staff.middle_c_at(5) == -6)
        # Test after bass clef goes into effect
        assert(test_staff.middle_c_at(15) == 6)

    def test_middle_c_at_with_implicit_default_clef(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        # No clef specified - should default to treble
        assert(test_staff.middle_c_at(5) == -6)

    def test_natural_midi_number_of_top_line_at_with_explicit_clefs(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        test_treble_clef = Clef(test_staff, 0,  'treble')
        test_bass_clef = Clef(test_staff, 10, 'bass')
        # Test between two clefs should be in treble mode
        assert(test_staff._natural_midi_number_of_top_line_at(5) == 77)
        # Test after bass clef goes into effect
        assert(test_staff._natural_midi_number_of_top_line_at(15) == 57)

    def test_natural_midi_number_of_top_line_at_with_implicit_default_clef(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        # No clef specified - should default to treble
        assert(test_staff._natural_midi_number_of_top_line_at(5) == 77)

    def test_position_outside_staff_with_odd_line_count(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=5)
        assert(test_staff._position_outside_staff(0) is False)
        assert(test_staff._position_outside_staff(4) is False)
        assert(test_staff._position_outside_staff(-4) is False)
        assert(test_staff._position_outside_staff(5) is True)
        assert(test_staff._position_outside_staff(-5) is True)

    def test_position_outside_staff_with_even_line_count(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=4)
        assert(test_staff._position_outside_staff(0) is False)
        assert(test_staff._position_outside_staff(3) is False)
        assert(test_staff._position_outside_staff(-3) is False)
        assert(test_staff._position_outside_staff(4) is True)
        assert(test_staff._position_outside_staff(-4) is True)

    def test_position_inside_staff_with_odd_line_count(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=5)
        assert(test_staff._position_inside_staff(0) is True)
        assert(test_staff._position_inside_staff(4) is True)
        assert(test_staff._position_inside_staff(-4) is True)
        assert(test_staff._position_inside_staff(5) is False)
        assert(test_staff._position_inside_staff(-5) is False)

    def test_position_inside_staff_with_even_line_count(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=4)
        assert(test_staff._position_inside_staff(0) is True)
        assert(test_staff._position_inside_staff(3) is True)
        assert(test_staff._position_inside_staff(-3) is True)
        assert(test_staff._position_inside_staff(4) is False)
        assert(test_staff._position_inside_staff(-4) is False)

    def test_position_on_ledger_with_odd_line_count(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=5)
        assert(test_staff._position_on_ledger(0) is False)
        assert(test_staff._position_on_ledger(4) is False)
        assert(test_staff._position_on_ledger(-4) is False)
        assert(test_staff._position_on_ledger(6) is True)
        assert(test_staff._position_on_ledger(-6) is True)
        assert(test_staff._position_on_ledger(7) is False)
        assert(test_staff._position_on_ledger(-7) is False)
        assert(test_staff._position_on_ledger(8) is True)
        assert(test_staff._position_on_ledger(-8) is True)

    def test_position_on_ledger_with_even_line_count(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=4)
        assert(test_staff._position_on_ledger(0) is False)
        assert(test_staff._position_on_ledger(3) is False)
        assert(test_staff._position_on_ledger(-3) is False)
        assert(test_staff._position_on_ledger(4) is False)
        assert(test_staff._position_on_ledger(-4) is False)
        assert(test_staff._position_on_ledger(5) is True)
        assert(test_staff._position_on_ledger(-5) is True)
        assert(test_staff._position_on_ledger(6) is False)
        assert(test_staff._position_on_ledger(-6) is False)
        assert(test_staff._position_on_ledger(7) is True)
        assert(test_staff._position_on_ledger(-7) is True)

    def test_ledgers_needed_from_position_with_odd_line_count(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=5)
        # Inside the staff, no ledgers
        assert(test_staff._ledgers_needed_from_position(0) == set())
        assert(test_staff._ledgers_needed_from_position(4) == set())
        assert(test_staff._ledgers_needed_from_position(-4) == set())
        # Just outside the staff, no ledgers
        assert(test_staff._ledgers_needed_from_position(5) == set())
        assert(test_staff._ledgers_needed_from_position(-5) == set())
        # Right on the first ledger
        assert(test_staff._ledgers_needed_from_position(6) == {6})
        assert(test_staff._ledgers_needed_from_position(-6) == {-6})
        # Far above or below, multiple ledgers
        assert(test_staff._ledgers_needed_from_position(10) == {6, 8, 10})
        assert(test_staff._ledgers_needed_from_position(-10) == {-6, -8, -10})
        assert(test_staff._ledgers_needed_from_position(11) == {6, 8, 10})
        assert(test_staff._ledgers_needed_from_position(-11) == {-6, -8, -10})

    def test_ledgers_needed_from_position_with_even_line_count(self):
        test_staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=4)
        # Inside the staff, no ledgers
        assert(test_staff._ledgers_needed_from_position(0) == set())
        assert(test_staff._ledgers_needed_from_position(3) == set())
        assert(test_staff._ledgers_needed_from_position(-3) == set())
        # Just outside the staff, no ledgers
        assert(test_staff._ledgers_needed_from_position(4) == set())
        assert(test_staff._ledgers_needed_from_position(-4) == set())
        # Right on the first ledger
        assert(test_staff._ledgers_needed_from_position(5) == {5})
        assert(test_staff._ledgers_needed_from_position(-5) == {-5})
        # Far above or below, multiple ledgers
        assert(test_staff._ledgers_needed_from_position(9) == {5, 7, 9})
        assert(test_staff._ledgers_needed_from_position(-9) == {-5, -7, -9})
        assert(test_staff._ledgers_needed_from_position(10) == {5, 7, 9})
        assert(test_staff._ledgers_needed_from_position(-10) == {-5, -7, -9})
