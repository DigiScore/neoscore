import unittest

import pytest

from neoscore.core import neoscore
from neoscore.core.flag import Flag, NoFlagNeededError
from neoscore.core.staff import Staff
from neoscore.models.beat import Beat
from neoscore.utils.units import Mm


class TestFlag(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.staff = Staff((Mm(0), Mm(0)), flowable=None, length=Mm(100))

    def test_glyphnames(self):
        # All flags with durations in the following denominations should
        # be init-able without error.
        for i in [1024, 512, 256, 128, 64, 32, 16, 8]:
            Flag(self.staff, Beat(1, i), 1)
            Flag(self.staff, Beat(1, i), -1)

    def test_invalid_direction_raises_value_error(self):
        with pytest.raises(ValueError):
            Flag(self.staff, Beat(1, 8), 0)
        with pytest.raises(ValueError):
            Flag(self.staff, Beat(1, 8), 2)
        with pytest.raises(ValueError):
            Flag(self.staff, Beat(1, 8), -2)

    def test_needs_flag(self):
        assert Flag.needs_flag(Beat(1, 4)) is False
        assert Flag.needs_flag(Beat(1, 2)) is False
        assert Flag.needs_flag(Beat(1, 8)) is True
        assert Flag.needs_flag(Beat(1, 16)) is True

    def test_vertical_offset_needed(self):
        self.assertEqual(
            Flag.vertical_offset_needed(Beat(1, 4), self.staff.unit), self.staff.unit(0)
        )

        self.assertEqual(
            Flag.vertical_offset_needed(Beat(1, 8), self.staff.unit), self.staff.unit(1)
        )

        self.assertEqual(
            Flag.vertical_offset_needed(Beat(1, 16), self.staff.unit),
            self.staff.unit(1),
        )

    def test_raises_no_flag_needed_error(self):
        # Test valid durations
        Flag(self.staff, Beat(1, 16), 1)
        Flag(self.staff, Beat(1, 8), 1)

        # Test invalid durations
        with pytest.raises(NoFlagNeededError):
            Flag(self.staff, Beat(1, 4), 1)
        with pytest.raises(NoFlagNeededError):
            Flag(self.staff, Beat(1, 2), 1)
        with pytest.raises(NoFlagNeededError):
            Flag(self.staff, Beat(1, 1), 1)
