import unittest

from neoscore import constants
from neoscore.core import neoscore
from neoscore.core.invisible_object import InvisibleObject
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.staff import Staff
from neoscore.utils.units import GraphicUnit, Mm, Unit


class TestMusicText(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.staff = Staff((Mm(0), Mm(0)), Mm(100), flowable=None, staff_unit=Mm(1))
        self.font = MusicFont(constants.DEFAULT_MUSIC_FONT_NAME, self.staff.unit)

    def test_init(self):
        mock_parent = InvisibleObject((Unit(10), Unit(11)), parent=self.staff)
        mtext = MusicText((Unit(5), Unit(6)), "accidentalFlat", mock_parent, self.font)
        assert mtext.x == GraphicUnit(5)
        assert mtext.y == GraphicUnit(6)
        assert mtext.text == "\ue260"
        assert mtext.font == self.font
        assert mtext.parent == mock_parent

    def test_init_with_one_tuple(self):
        mtext = MusicText((Unit(5), Unit(6)), ("brace", 1), self.staff)
        assert mtext.text == "\uF400"

    def test_init_with_one_music_char(self):
        mtext = MusicText(
            (Unit(5), Unit(6)), MusicChar(self.staff.music_font, "brace", 1), self.staff
        )
        assert mtext.text == "\uF400"

    def test_init_with_multiple_chars_in_list(self):
        mtext = MusicText(
            (Unit(5), Unit(6)), ["accidentalFlat", ("brace", 1)], self.staff
        )
        assert mtext.text == "\ue260\uF400"

    def test_text_setter(self):
        mtext = MusicText((Unit(5), Unit(6)), "accidentalSharp", self.staff)
        assert mtext.text == "\ue262"
        mtext.text = "accidentalFlat"
        assert mtext.text == "\ue260"
