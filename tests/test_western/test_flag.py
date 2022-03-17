import unittest

import pytest

from neoscore.core import neoscore
from neoscore.models.beat import Beat
from neoscore.utils.point import ORIGIN
from neoscore.utils.units import Mm
from neoscore.western.flag import Flag, NoFlagNeededError
from neoscore.western.staff import Staff


class TestFlag(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.staff = Staff((Mm(0), Mm(0)), None, length=Mm(100))

    def test_glyphnames(self):
        # All flags with durations in the following denominations should
        # be init-able without error.
        for i in [1024, 512, 256, 128, 64, 32, 16, 8]:
            Flag(ORIGIN, self.staff, Beat(1, i), 1)
            Flag(ORIGIN, self.staff, Beat(1, i), -1)

    def test_needs_flag(self):
        assert Flag.needs_flag(Beat(1, 4)) is False
        assert Flag.needs_flag(Beat(1, 2)) is False
        assert Flag.needs_flag(Beat(1, 8)) is True
        assert Flag.needs_flag(Beat(1, 16)) is True

    def test_vertical_offset_needed(self):
        assert Flag.vertical_offset_needed(Beat(1, 4)) == 0
        assert Flag.vertical_offset_needed(Beat(1, 8)) == 1
        assert Flag.vertical_offset_needed(Beat(1, 16)) == 1

    def test_raises_no_flag_needed_error(self):
        # Test valid durations
        Flag(ORIGIN, self.staff, Beat(1, 16), 1)
        Flag(ORIGIN, self.staff, Beat(1, 8), 1)

        # Test invalid durations
        with pytest.raises(NoFlagNeededError):
            Flag(ORIGIN, self.staff, Beat(1, 4), 1)
        with pytest.raises(NoFlagNeededError):
            Flag(ORIGIN, self.staff, Beat(1, 2), 1)
        with pytest.raises(NoFlagNeededError):
            Flag(ORIGIN, self.staff, Beat(1, 1), 1)
