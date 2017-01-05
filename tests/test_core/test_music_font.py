import os
import unittest

from brown.config import config
from brown.core import brown
from brown.core.music_font import MusicFont
from brown.primitives.staff import Staff
from brown.utils.units import GraphicUnit, Mm


class TestMusicFont(unittest.TestCase):

    def setUp(self):
        brown.setup()
        font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        metadata_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'bravura_metadata.json')
        self.font_id = brown.register_music_font(
            font_file_path, metadata_file_path)
        self.staff = Staff((Mm(0), Mm(0)), Mm(100),
                           frame=None, staff_unit=Mm(1))

    def test_init(self):
        test_font = MusicFont('Bravura', self.staff.unit)
        assert(test_font.family_name == 'Bravura')
        assert(test_font.size == float(GraphicUnit(self.staff.unit(3))))
        assert(test_font.em_size == test_font.size)
        assert(test_font.weight == 1)      # Set automatically by initializer
        assert(test_font.italic is False)  # Set automatically by initializer
