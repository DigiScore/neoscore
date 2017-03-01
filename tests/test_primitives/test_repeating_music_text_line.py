import unittest

from brown.core import brown
from brown.utils.units import Mm
from brown.core.flowable_frame import FlowableFrame
from brown.core.music_text_object import MusicTextObject
from brown.primitives.staff import Staff
from brown.primitives.repeating_music_text_line import RepeatingMusicTextLine

from mock_staff_object import MockStaffObject


class TestRepeatingMusicTextLine(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(5000), self.frame)
        self.left_parent = MockStaffObject((Mm(0), Mm(0)), self.staff)
        self.right_parent = MockStaffObject((Mm(10), Mm(2)), self.staff)
        self.char = 'gClef'
        self.single_repetition_width = MusicTextObject(
            (Mm(0), Mm(0)),
            self.char,
            self.left_parent,
            scale_factor=2)._bounding_rect.width

    def test_repetition_count(self):
        line = RepeatingMusicTextLine((Mm(1), Mm(2), 0, self.left_parent),
                                      (Mm(3), Mm(0), 0, self.right_parent),
                                      self.char,
                                      scale_factor=2)
        expected = int(Mm(12) / self.single_repetition_width)
        assert(line._repetitions_needed == expected)
