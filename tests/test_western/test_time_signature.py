import unittest

from neoscore.core import neoscore
from neoscore.core.music_char import MusicChar
from neoscore.utils.point import ORIGIN
from neoscore.utils.units import ZERO, Mm
from neoscore.western.meter import COMMON_TIME, CUT_TIME, Meter
from neoscore.western.staff import Staff
from neoscore.western.time_signature import TimeSignature
from tests.helpers import render_scene

# TODO LOW test that glyphs are actually created successfully - this
# failed to catch bugs in creating rhythm dots and flags, and probably
# fails to catch other similar ones too.


class TestChordrest(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.staff = Staff(ORIGIN, None, Mm(100))

    def test_with_single_digit_numeric_meter(self):
        ts = TimeSignature(ZERO, self.staff, Meter.numeric(3, 4))
        assert ts.upper_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig3")
        ]
        assert ts.lower_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig4")
        ]

    def test_with_multi_digit_numeric_meter(self):
        ts = TimeSignature(ZERO, self.staff, Meter.numeric(12, 16))
        assert ts.upper_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig1"),
            MusicChar(self.staff.music_font, "timeSig2"),
        ]
        assert ts.lower_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig1"),
            MusicChar(self.staff.music_font, "timeSig6"),
        ]

    def test_with_additive_numeric_meter(self):
        ts = TimeSignature(ZERO, self.staff, Meter.numeric([5, 10], 16))
        assert ts.upper_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig5"),
            MusicChar(self.staff.music_font, "timeSigPlus"),
            MusicChar(self.staff.music_font, "timeSig1"),
            MusicChar(self.staff.music_font, "timeSig0"),
        ]
        assert ts.lower_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig1"),
            MusicChar(self.staff.music_font, "timeSig6"),
        ]

    def test_with_shorthand_meter(self):
        ts = TimeSignature(ZERO, self.staff, (3, 4))
        assert ts.upper_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig3")
        ]
        assert ts.lower_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig4")
        ]

    def test_with_common_time(self):
        ts = TimeSignature(ZERO, self.staff, COMMON_TIME)
        assert ts.upper_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSigCommon")
        ]
        assert ts.lower_text.music_chars == []

    def test_with_cut_time(self):
        ts = TimeSignature(ZERO, self.staff, CUT_TIME)
        assert ts.upper_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSigCutCommon")
        ]
        assert ts.lower_text.music_chars == []

    def test_meter_setter_updates_glyphs(self):
        ts = TimeSignature(ZERO, self.staff, CUT_TIME)
        ts.meter = (3, 4)
        assert ts.upper_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig3")
        ]
        assert ts.lower_text.music_chars == [
            MusicChar(self.staff.music_font, "timeSig4")
        ]

    def test_end_to_end(self):
        ts = TimeSignature(ZERO, self.staff, COMMON_TIME)
        render_scene()
