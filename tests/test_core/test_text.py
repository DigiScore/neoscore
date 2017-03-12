import os
import unittest

from brown.core import brown
from brown.core.text import Text
from brown import config
from brown.core.font import Font

from tests.mocks.mock_graphic_object import MockGraphicObject


class TestText(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.test_font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        self.font_id = brown._app_interface.register_font(
            self.test_font_file_path)
        self.font = Font('Bravura', 12, 1, False)

    def test_init(self):
        mock_parent = MockGraphicObject((10, 11), parent=None)
        test_object = Text((5, 6), 'testing', self.font, mock_parent)
        assert(test_object.x == 5)
        assert(test_object.y == 6)
        assert(test_object.text == 'testing')
        assert(test_object.font == self.font)
        assert(test_object.parent == mock_parent)

    def test_default_init_values(self):
        # API default values canary
        test_object = Text((5, 6), 'testing')
        assert(test_object.font == brown.text_font)
        assert(test_object.parent == brown.document)
