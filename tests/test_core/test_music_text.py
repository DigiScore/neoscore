import unittest

from neoscore import constants
from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.pen import Pen
from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.rect import Rect
from neoscore.utils.units import ZERO, Mm, Unit
from neoscore.western.staff import Staff


class TestMusicText(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.staff = Staff((Mm(0), Mm(0)), None, length=Mm(100), staff_unit=Mm(1))
        self.font = MusicFont(constants.DEFAULT_MUSIC_FONT_NAME, self.staff.unit)

    def test_init(self):
        pen = Pen("#00ff00")
        brush = Brush("#ff0000")
        mock_parent = PositionedObject((Unit(10), Unit(11)), self.staff)
        mtext = MusicText(
            (Unit(5), Unit(6)),
            mock_parent,
            "accidentalFlat",
            self.font,
            brush,
            pen,
            2,
            False,
        )
        assert mtext.pos == Point(Unit(5), Unit(6))
        assert mtext.parent == mock_parent
        assert mtext.text == "\ue260"
        assert mtext.font == self.font
        assert mtext.brush == brush
        assert mtext.pen == pen

    def test_init_with_one_tuple(self):
        mtext = MusicText((Unit(5), Unit(6)), self.staff, ("brace", 1))
        assert mtext.text == "\uF400"

    def test_init_with_one_music_char(self):
        mtext = MusicText(
            (Unit(5), Unit(6)), self.staff, MusicChar(self.staff.music_font, "brace", 1)
        )
        assert mtext.text == "\uF400"

    def test_init_with_multiple_chars_in_list(self):
        mtext = MusicText(
            (Unit(5), Unit(6)), self.staff, ["accidentalFlat", ("brace", 1)]
        )
        assert mtext.text == "\ue260\uF400"

    def test_init_with_empty_str(self):
        mtext = MusicText(ORIGIN, self.staff, "")
        assert mtext.text == ""
        assert mtext.music_chars == []
        bounding_rect = mtext.bounding_rect
        assert bounding_rect == Rect(ZERO, ZERO, ZERO, ZERO)

    def test_text_setter(self):
        mtext = MusicText((Unit(5), Unit(6)), self.staff, "accidentalSharp")
        assert mtext.text == "\ue262"
        mtext.text = "accidentalFlat"
        assert mtext.text == "\ue260"
        assert mtext.music_chars == [MusicChar(self.font, "accidentalFlat")]

    def test_music_chars_setter(self):
        mtext = MusicText((Unit(5), Unit(6)), self.staff, "accidentalSharp")
        assert mtext.music_chars == [MusicChar(self.font, "accidentalSharp")]
        assert mtext.text == "\ue262"
        new_chars = [MusicChar(self.font, "accidentalFlat")]
        mtext.music_chars = new_chars
        assert mtext.music_chars == new_chars
        # text should be updated too
        assert mtext.text == "\ue260"

    def test_breakable_passed_to_superclass(self):
        mtext = MusicText((Unit(5), Unit(6)), self.staff, "accidentalSharp")
        assert mtext.breakable == True
