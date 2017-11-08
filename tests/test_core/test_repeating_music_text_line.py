import unittest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.music_text import MusicText
from brown.core.repeating_music_text_line import RepeatingMusicTextLine
from brown.core.staff import Staff
from brown.utils.units import Mm
from tests.mocks.mock_staff_object import MockStaffObject


class TestRepeatingMusicTextLine(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(5000), self.flowable)
        self.left_parent = MockStaffObject((Mm(0), Mm(0)), self.staff)
        self.right_parent = MockStaffObject((Mm(10), Mm(2)), self.staff)
        self.char = 'gClef'
        self.single_repetition_width = MusicText(
            (Mm(0), Mm(0)),
            self.char,
            self.staff,
            scale_factor=2).bounding_rect.width

    def test_repetition_count(self):
        line = RepeatingMusicTextLine((Mm(1), Mm(2)),
                                      self.left_parent,
                                      Mm(3),
                                      self.char,
                                      self.right_parent,
                                      scale_factor=2)
        expected = int(Mm(12) / self.single_repetition_width)
        assert(line._repetitions_needed == expected)
