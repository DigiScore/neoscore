import os
import unittest

from nose.tools import assert_raises, nottest

from brown.core import brown
from brown.core.music_glyph import MusicGlyph
from brown.config import config
from brown.core.font import Font
from brown.core.music_font import MusicFont

from mock_graphic_object import MockGraphicObject


class TestGlyph(unittest.TestCase):

    def setUp(self):
        brown.setup()
        font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        metadata_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'bravura_metadata.json')
        self.font_id = brown.register_music_font(
            font_file_path, metadata_file_path)
        self.font = MusicFont('Bravura', 35)

    def test_init(self):
        mock_parent = MockGraphicObject((10, 11), parent=None)
        test_object = MusicGlyph((5, 6), 'accidentalFlat', self.font, mock_parent)
        assert(test_object.x == 5)
        assert(test_object.y == 6)
        assert(test_object.text == '\ue260')
        assert(test_object.font == self.font)
        assert(test_object.parent == mock_parent)

    @nottest
    def test_non_music_font_raises_error(self):
        # Depending on implementation decision in MusicGlyph, this may or may
        # not be needed
        with assert_raises(TypeError):
            normal_font = Font('Bravura', 12, 2, False)
            MusicGlyph((5, 6), 'accidentalFlat', normal_font)
