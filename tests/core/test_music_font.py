import os
import unittest

from brown.config import config
from brown.core import brown
from brown.core.music_font import MusicFont
from brown.utils.units import GraphicUnit


class TestMusicFont(unittest.TestCase):

    def setUp(self):
        brown.setup()
        font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        metadata_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'bravura_metadata.json')
        self.font_id = brown.register_music_font(
            font_file_path, metadata_file_path)

    def test_init(self):
        test_font = MusicFont('Bravura', 35)
        assert(test_font.family_name == 'Bravura')
        assert(test_font.size == 35)
        assert(test_font.weight == 1)      # Set automatically by initializer
        assert(test_font.italic is False)  # Set automatically by initializer
        self.assertAlmostEqual(
            test_font.em_size, GraphicUnit(48))

    def test_calculate_approximate_em_size(self):
        test_font = MusicFont('Bravura', 35)
        self.assertAlmostEqual(
            test_font._calculate_approximate_em_size(), GraphicUnit(48))
