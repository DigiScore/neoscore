import unittest
import pytest

from brown.core import brown
from brown.primitives.notehead import Notehead
from brown.primitives.staff import Staff


"""


Continue work on this once safe ways to teardown the Qt app
are worked out to allow testing.


"""

@pytest.mark.skip
class TestNotehead(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def tearDown(self):
        # TODO: After implementing proper app interface
        #       teardown, use this
        #pass
        #brown.exec_()
        brown._app_interface.app.exit()

    def test_staff_position_middle_c_treble(self):
        mock_staff = Staff(0, 0, 100)
        assert(Notehead(mock_staff, 50, "c'").staff_position == -6)

    def test_staff_position_low_octaves(self):
        mock_staff = Staff(0, 0, 100)
        assert(Notehead(mock_staff, 50, "c").staff_position == -14)
        assert(Notehead(mock_staff, 50, "c,").staff_position == -22)
        assert(Notehead(mock_staff, 50, "c,,").staff_position == -30)
        assert(Notehead(mock_staff, 50, "c,,,").staff_position == -38)

    def test_staff_position_high_octaves(self):
        mock_staff = Staff(0, 0, 100)
        assert(Notehead(mock_staff, 50, "c'").staff_position == -6)
        assert(Notehead(mock_staff, 50, "c''").staff_position == 2)
        assert(Notehead(mock_staff, 50, "c'''").staff_position == 10)
        assert(Notehead(mock_staff, 50, "c''''").staff_position == 18)
        assert(Notehead(mock_staff, 50, "c'''''").staff_position == 26)

    def test_staff_position_with_accidentals(self):
        mock_staff = Staff(0, 0, 100)
        assert(Notehead(mock_staff, 50, "cf'").staff_position == -6)
        assert(Notehead(mock_staff, 50, "cn'").staff_position == -6)
        assert(Notehead(mock_staff, 50, "cs'").staff_position == -6)

    def test_staff_position_with_all_letter_names(self):
        mock_staff = Staff(0, 0, 100)
        assert(Notehead(mock_staff, 50, "c'").staff_position == -6)
        assert(Notehead(mock_staff, 50, "d'").staff_position == -5)
        assert(Notehead(mock_staff, 50, "e'").staff_position == -4)
        assert(Notehead(mock_staff, 50, "f'").staff_position == -3)
        assert(Notehead(mock_staff, 50, "g'").staff_position == -2)
        assert(Notehead(mock_staff, 50, "a'").staff_position == -1)
        assert(Notehead(mock_staff, 50, "b'").staff_position == 0)
