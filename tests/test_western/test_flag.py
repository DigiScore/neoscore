import pytest

from neoscore.core.directions import DirectionY
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm
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
            Flag(ORIGIN, self.staff, Duration(1, i), DirectionY.DOWN)
            Flag(ORIGIN, self.staff, Duration(1, i), DirectionY.UP)

    def test_glyph_selection(self):
        flag = Flag(ORIGIN, self.staff, Duration(1, 32), DirectionY.DOWN)
        assert flag.music_chars == [MusicChar(self.staff.music_font, "flag32ndDown")]
        flag = Flag(ORIGIN, self.staff, Duration(1, 16), DirectionY.UP)
        assert flag.music_chars == [MusicChar(self.staff.music_font, "flag16thUp")]

    def test_font_override(self):
        font = MusicFont("Bravura", Mm(3))
        flag = Flag(ORIGIN, self.staff, Duration(1, 32), DirectionY.DOWN, font)
        assert flag.music_font == font

    def test_vertical_offset_needed(self):
        assert Flag.vertical_offset_needed(Duration(1, 4)) == 0
        assert Flag.vertical_offset_needed(Duration(1, 8)) == 1
        assert Flag.vertical_offset_needed(Duration(1, 16)) == 1

    def test_raises_no_flag_needed_error(self):
        # Test valid durations
        Flag(ORIGIN, self.staff, Duration(1, 16), DirectionY.DOWN)
        Flag(ORIGIN, self.staff, Duration(1, 8), DirectionY.DOWN)

        # Test invalid durations
        with pytest.raises(NoFlagNeededError):
            Flag(ORIGIN, self.staff, Duration(1, 4), DirectionY.DOWN)
        with pytest.raises(NoFlagNeededError):
            Flag(ORIGIN, self.staff, Duration(1, 2), DirectionY.DOWN)
        with pytest.raises(NoFlagNeededError):
            Flag(ORIGIN, self.staff, Duration(1, 1), DirectionY.DOWN)
