import unittest

from brown import config
from brown.core import brown
from brown.core.music_font import MusicFont
from brown.core.staff import Staff
from brown.utils.units import Mm


class TestMusicFont(unittest.TestCase):

    def setUp(self):
        brown.setup()
        brown.register_music_font(config.DEFAULT_MUSIC_FONT_NAME,
                                  config.DEFAULT_MUSIC_FONT_PATH,
                                  config.DEFAULT_MUSIC_FONT_METADATA_PATH)
        self.staff = Staff((Mm(0), Mm(0)), Mm(100),
                           frame=None, staff_unit=Mm(1))

    def test_init(self):
        test_font = MusicFont(config.DEFAULT_MUSIC_FONT_NAME, self.staff.unit)
        assert(test_font.family_name == config.DEFAULT_MUSIC_FONT_NAME)
        assert(test_font.size == self.staff.unit(3))
        assert(test_font.em_size == test_font.size)
        assert(test_font.weight == 1)      # Set default by initializer
        assert(test_font.italic is False)  # Set default by initializer
