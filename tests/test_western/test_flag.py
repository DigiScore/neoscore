import pytest

from neoscore.core.directions import VerticalDirection
from neoscore.core.music_char import MusicChar
from neoscore.utils.point import ORIGIN
from neoscore.utils.units import Mm
from neoscore.western.duration import Duration
from neoscore.western.flag import Flag, NoFlagNeededError
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestFlag(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff((Mm(0), Mm(0)), None, length=Mm(100))

    def test_glyphname_lookup_for_all_durs_succeeds(self):
        # All flags with durations in the following denominations should
        # be init-able without error.
        for i in [1024, 512, 256, 128, 64, 32, 16, 8]:
            Flag(ORIGIN, self.staff, Duration(1, i), VerticalDirection.DOWN)
            Flag(ORIGIN, self.staff, Duration(1, i), VerticalDirection.UP)

    def test_glyph_selection(self):
        flag = Flag(ORIGIN, self.staff, Duration(1, 32), VerticalDirection.DOWN)
        assert flag.music_chars == [MusicChar(self.staff.music_font, "flag32ndDown")]
        flag = Flag(ORIGIN, self.staff, Duration(1, 16), VerticalDirection.UP)
        assert flag.music_chars == [MusicChar(self.staff.music_font, "flag16thUp")]

    def test_vertical_offset_needed(self):
        assert Flag.vertical_offset_needed(Duration(1, 4)) == 0
        assert Flag.vertical_offset_needed(Duration(1, 8)) == 1
        assert Flag.vertical_offset_needed(Duration(1, 16)) == 1

    def test_raises_no_flag_needed_error(self):
        # Test valid durations
        Flag(ORIGIN, self.staff, Duration(1, 16), VerticalDirection.DOWN)
        Flag(ORIGIN, self.staff, Duration(1, 8), VerticalDirection.DOWN)

        # Test invalid durations
        with pytest.raises(NoFlagNeededError):
            Flag(ORIGIN, self.staff, Duration(1, 4), VerticalDirection.DOWN)
        with pytest.raises(NoFlagNeededError):
            Flag(ORIGIN, self.staff, Duration(1, 2), VerticalDirection.DOWN)
        with pytest.raises(NoFlagNeededError):
            Flag(ORIGIN, self.staff, Duration(1, 1), VerticalDirection.DOWN)
