import os
import unittest

from brown.core import brown
from brown.core.text_object import TextObject
from brown.config import config
from brown.core.font import Font

from mock_graphic_object import MockGraphicObject


class TestTextObject(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.test_font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        self.font_id = brown._app_interface.register_font(
            self.test_font_file_path)
        self.font = Font('Bravura', 12, 1, False)

    def test_init(self):
        mock_parent = MockGraphicObject(10, 11, parent=None)
        test_object = TextObject(5, 6, 'testing', self.font, mock_parent)
        assert(test_object.x == 5)
        assert(test_object.y == 6)
        assert(test_object.text == 'testing')
        assert(test_object.font == self.font)
        assert(test_object.parent == mock_parent)

    def test_default_init_values(self):
        # API default values canary
        test_object = TextObject(5, 6, 'testing')
        # When no font is passed, the global brown default text_font is used
        assert(test_object.font == brown.text_font)
        assert(test_object.parent is None)

    def test_text_setter_changes_interface(self):
        test_object = TextObject(5, 6, 'testing')
        test_object.text = 'new value'
        assert(test_object.text == 'new value')
        assert(test_object._interface.text == 'new value')

    def test_font_setter_changes_interface(self):
        test_object = TextObject(5, 6, 'testing')
        new_font = Font('Bravura', 20, 1, False)
        test_object.font = new_font
        assert(test_object.font == new_font)
        assert(test_object._interface.font == new_font._interface)
