from neoscore.core.flowable import Flowable
from neoscore.core.music_char import MusicChar
from neoscore.core.music_text import MusicText
from neoscore.utils.point import ORIGIN
from neoscore.utils.units import Mm
from neoscore.western.repeating_music_text_line import RepeatingMusicTextLine
from neoscore.western.staff import Staff
from tests.mocks.mock_staff_object import MockStaffObject

from ..helpers import AppTest


class TestRepeatingMusicTextLine(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(5000))
        self.left_parent = MockStaffObject((Mm(0), Mm(0)), self.staff)
        self.right_parent = MockStaffObject((Mm(10), Mm(2)), self.staff)
        self.char = "gClef"
        self.single_repetition_width = MusicText(
            (Mm(0), Mm(0)), self.staff, self.char
        ).bounding_rect.width

    def test_without_end_cap_text(self):
        line = RepeatingMusicTextLine(
            (Mm(1), Mm(2)),
            self.left_parent,
            (Mm(3), Mm(-2)),
            self.right_parent,
            self.char,
        )
        expected_reps = int(Mm(12) / self.single_repetition_width)
        assert len(line.music_chars) == expected_reps
        self.assertAlmostEqual(line.rotation, -9.462322208025618)
        assert line.rotation == line.angle

    def test_with_end_cap_text(self):
        line = RepeatingMusicTextLine(
            ORIGIN,
            self.staff,
            (Mm(5), Mm(-10)),
            None,
            "wiggleArpeggiatoUp",
            "wiggleArpeggiatoUpArrow",
        )
        assert len(line.music_chars) == 7
        for char in line.music_chars[:-1]:
            assert char == MusicChar(self.staff.music_font, "wiggleArpeggiatoUp")
        assert line.music_chars[-1] == MusicChar(
            self.staff.music_font, "wiggleArpeggiatoUpArrow"
        )
