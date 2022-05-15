import pytest

from neoscore.core.brush import Brush
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN
from neoscore.core.repeating_music_text_line import RepeatingMusicTextLine
from neoscore.core.units import Inch, Mm
from neoscore.western.staff import Staff
from tests.helpers import AppTest
from tests.mocks.mock_staff_object import MockStaffObject


@pytest.mark.skipif("not AppTest.running_on_linux()")
class TestRepeatingMusicTextLine(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff((Mm(0), Mm(0)), None, Mm(5000))

    def test_without_end_cap_text(self):
        left_parent = MockStaffObject((Mm(0), Mm(0)), self.staff)
        right_parent = MockStaffObject((Mm(10), Mm(2)), self.staff)
        char = "gClef"
        line = RepeatingMusicTextLine(
            (Mm(1), Mm(2)),
            left_parent,
            (Mm(3), Mm(-2)),
            right_parent,
            char,
        )
        assert len(line.music_chars) == 3
        self.assertAlmostEqual(line.rotation, -9.462322208025618)
        assert line.rotation == line.angle

    def test_with_start_cap_text(self):
        line = RepeatingMusicTextLine(
            ORIGIN,
            self.staff,
            (Mm(5), Mm(-10)),
            None,
            "wiggleTrill",
            "ornamentTrill",
        )
        assert len(line.music_chars) == 5
        for char in line.music_chars[1:]:
            assert char == MusicChar(self.staff.music_font, "wiggleTrill")
        assert line.music_chars[0] == MusicChar(self.staff.music_font, "ornamentTrill")

    def test_with_end_cap_text(self):
        line = RepeatingMusicTextLine(
            ORIGIN,
            self.staff,
            (Mm(5), Mm(-10)),
            None,
            "wiggleArpeggiatoUp",
            None,
            "wiggleArpeggiatoUpArrow",
        )
        assert len(line.music_chars) == 5
        for char in line.music_chars[:-1]:
            assert char == MusicChar(self.staff.music_font, "wiggleArpeggiatoUp")
        assert line.music_chars[-1] == MusicChar(
            self.staff.music_font, "wiggleArpeggiatoUpArrow"
        )

    def test_font_defaults_to_parent(self):
        line = RepeatingMusicTextLine(
            ORIGIN, self.staff, (Mm(5), Mm(-10)), None, "gClef"
        )
        assert line.music_font == self.staff.music_font

    def test_font_override(self):
        font = MusicFont("Bravura", Inch)
        line = RepeatingMusicTextLine(
            ORIGIN, self.staff, (Mm(5), Mm(-10)), None, "gClef", font=font
        )
        assert line.music_font == font

    def test_brush_default(self):
        line = RepeatingMusicTextLine(
            ORIGIN, self.staff, (Mm(5), Mm(-10)), None, "gClef"
        )
        assert line.brush == Brush()

    def test_brush_override(self):
        line = RepeatingMusicTextLine(
            ORIGIN, self.staff, (Mm(5), Mm(-10)), None, "gClef", brush="#ff0000"
        )
        assert line.brush == Brush("#ff0000")

    def test_pen_default_is_no_pen(self):
        line = RepeatingMusicTextLine(
            ORIGIN, self.staff, (Mm(5), Mm(-10)), None, "gClef"
        )
        assert line.pen == Pen.no_pen()

    def test_pen_override(self):
        line = RepeatingMusicTextLine(
            ORIGIN, self.staff, (Mm(5), Mm(-10)), None, "gClef", pen="#ff0000"
        )
        assert line.pen == Pen("#ff0000")

    def test_background_brush_default(self):
        line = RepeatingMusicTextLine(
            ORIGIN, self.staff, (Mm(5), Mm(-10)), None, "gClef"
        )
        assert line.background_brush is None

    def test_background_brush_override(self):
        line = RepeatingMusicTextLine(
            ORIGIN,
            self.staff,
            (Mm(5), Mm(-10)),
            None,
            "gClef",
            background_brush="#ff0000",
        )
        assert line.background_brush == Brush("#ff0000")
