from neoscore.core.music_char import MusicChar
from neoscore.core.point import ORIGIN
from neoscore.core.units import ZERO, Mm
from neoscore.western.meter import COMMON_TIME, CUT_TIME, Meter
from neoscore.western.staff import Staff
from neoscore.western.time_signature import TimeSignature
from tests.helpers import render_scene

from ..helpers import AppTest


class TestTimeSignature(AppTest):
    def setUp(self):
        super().setUp()
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

    def test_alignment_lower_needing_adjustment(self):
        ts = TimeSignature(ZERO, self.staff, Meter.numeric([5, 10], 16))
        assert ts.upper_text.x == ZERO
        assert ts.lower_text.x > ZERO  # Exact values flake..

    def test_alignment_upper_needing_adjustment(self):
        ts = TimeSignature(ZERO, self.staff, Meter.numeric(1, 16))
        assert ts.lower_text.x == ZERO
        assert ts.upper_text.x > ZERO  # Exact values flake..

    def test_single_glyph_centered(self):
        ts = TimeSignature(ZERO, self.staff, COMMON_TIME)
        assert ts.upper_text.y == self.staff.unit(2)

    def test_meter_setter_updates_alignment(self):
        ts = TimeSignature(ZERO, self.staff, CUT_TIME)
        assert ts.upper_text.y == self.staff.unit(2)
        ts.meter = (3, 4)
        assert ts.upper_text.y == self.staff.unit(1)
        assert ts.lower_text.y == self.staff.unit(3)

    def test_width_set_to_max_text_width(self):
        ts = TimeSignature(ZERO, self.staff, Meter.numeric([5, 10], 16))
        assert ts.visual_width == ts.upper_text.bounding_rect.width

    def test_meter_setter_updates_width(self):
        ts = TimeSignature(ZERO, self.staff, CUT_TIME)
        assert ts.visual_width == ts.upper_text.bounding_rect.width
        ts.meter = (3, 4)
        assert ts.visual_width == ts.lower_text.bounding_rect.width

    def test_end_to_end(self):
        ts = TimeSignature(ZERO, self.staff, COMMON_TIME)
        render_scene()
