import unittest
from nose.tools import assert_raises

from brown.core import brown
from brown.utils.units import Mm
from brown.core.paper import Paper
from brown.core.flowable_frame import FlowableFrame
from brown.primitives.staff import Staff, NoClefError
from brown.primitives.clef import Clef


class TestStaff(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_height(self):
        # 5 lines
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100),
                  self.frame, staff_unit=Mm(1.5), line_count=5).height,
            Mm(6))
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100),
                  self.frame, staff_unit=Mm(1), line_count=5).height,
            Mm(4))
        # 4 lines
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100),
                  self.frame, staff_unit=Mm(1.5), line_count=4).height,
            Mm(4.5))
        self.assertAlmostEqual(
            Staff((Mm(0), Mm(0)), Mm(100),
                  self.frame, staff_unit=Mm(1), line_count=4).height,
            Mm(3))

    def test_active_clef_at_with_explicit_clefs(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        staff.add_clef((0, 4), 'treble')
        staff.add_clef((2, 4), 'bass')
        # Test between two clefs should have treble in effect
        assert(staff.active_clef_at(staff.beat(1, 4)).clef_type == 'treble')
        # Test after bass clef goes into effect
        assert(staff.active_clef_at(staff.beat(3, 4)).clef_type == 'bass')

    def test_active_clef_at_with_implicit_default_clef(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        assert(staff.active_clef_at(Mm(5)) is None)

    def test_middle_c_at_with_explicit_clefs(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        staff.add_clef((0, 4), 'treble')
        staff.add_clef((2, 4), 'bass')
        # Test between two clefs should be in treble mode
        assert(staff.middle_c_at(staff.beat(1, 4)) == staff.unit(5))
        # Test after bass clef goes into effect
        assert(staff.middle_c_at(staff.beat(3, 4)) == staff.unit(-1))

    def test_middle_c_at_with_implicit_default_clef(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        with assert_raises(NoClefError):
            staff.middle_c_at(Mm(5))

    def test_natural_midi_number_of_top_line_at_with_explicit_clefs(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        staff.add_clef((0, 4), 'treble')
        staff.add_clef((2, 4), 'bass')
        # Test between two clefs should be in treble mode
        assert(staff._natural_midi_number_of_top_line_at(staff.beat(1, 4)) == 77)
        # Test after bass clef goes into effect
        assert(staff._natural_midi_number_of_top_line_at(staff.beat(3, 4)) == 57)

    def test_natural_midi_number_of_top_line_at_with_implicit_default_clef(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame)
        # No clef specified - should default to treble
        assert(staff._natural_midi_number_of_top_line_at(5) == 77)

    def test_position_outside_staff_is_inverse_of_inside(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=4)
        i = -1
        while i < 5:
            assert(staff._position_outside_staff(staff.unit(i)) !=
                   staff._position_inside_staff(staff.unit(i)))
            i += 1

    def test_position_inside_staff_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=5)
        assert(staff._position_inside_staff(staff.unit(0)) is True)
        assert(staff._position_inside_staff(staff.unit(4)) is True)
        assert(staff._position_inside_staff(staff.unit(5)) is False)
        assert(staff._position_inside_staff(staff.unit(-5)) is False)

    def test_position_inside_staff_with_even_line_count(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=4)
        assert(staff._position_inside_staff(staff.unit(0)) is True)
        assert(staff._position_inside_staff(staff.unit(3)) is True)
        assert(staff._position_inside_staff(staff.unit(4)) is False)
        assert(staff._position_inside_staff(staff.unit(-4)) is False)

    def test_position_on_ledger_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=5)
        assert(staff._position_on_ledger(staff.unit(-1)) is True)
        assert(staff._position_on_ledger(staff.unit(-0.5)) is False)
        assert(staff._position_on_ledger(staff.unit(0)) is False)
        assert(staff._position_on_ledger(staff.unit(4)) is False)
        assert(staff._position_on_ledger(staff.unit(4.5)) is False)
        assert(staff._position_on_ledger(staff.unit(5)) is True)

    def test_ledgers_needed_from_position_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), Mm(100), self.frame, line_count=5)
        # Inside the staff, no ledgers
        assert(staff._ledgers_needed_from_position(staff.unit(0)) == set())
        assert(staff._ledgers_needed_from_position(staff.unit(4)) == set())
        # Just outside the staff, no ledgers
        assert(staff._ledgers_needed_from_position(staff.unit(-0.5)) == set())
        assert(staff._ledgers_needed_from_position(staff.unit(4.5)) == set())
        # Right on the first ledger
        assert(staff._ledgers_needed_from_position(staff.unit(-1)) ==
               {staff.unit(-1)})
        assert(staff._ledgers_needed_from_position(staff.unit(5)) ==
               {staff.unit(5)})
        # Further outside with multiple ledgers, directly on lines
        assert(staff._ledgers_needed_from_position(staff.unit(6)) ==
               {staff.unit(6), staff.unit(5)})
        assert(staff._ledgers_needed_from_position(staff.unit(-2)) ==
               {staff.unit(-2), staff.unit(-1)})
        # Further outside with multiple ledgers, between lines
        assert(staff._ledgers_needed_from_position(staff.unit(6.5)) ==
               {staff.unit(6), staff.unit(5)})
        assert(staff._ledgers_needed_from_position(staff.unit(-2.5)) ==
               {staff.unit(-2), staff.unit(-1)})
