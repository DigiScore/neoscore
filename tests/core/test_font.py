import os
import unittest

from brown.config import config
from brown.core import brown
from brown.core.font import Font


class TestFont(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.test_font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        self.font_id = brown._app_interface.register_font(
            self.test_font_file_path)

    def test_init(self):
        test_font = Font('Bravura', 12, 2, False)
        assert(test_font.family_name == 'Bravura')
        assert(test_font.size == 12)
        assert(test_font.weight == 2)
        assert(test_font.italic is False)
        assert(test_font._interface.family_name == 'Bravura')
        assert(test_font._interface.size == 12)
        assert(test_font._interface.weight == 2)
        assert(test_font._interface.italic is False)

    def test_default_init_values(self):
        # API default values canary
        test_font = Font('Bravura', 12)
        assert(test_font.weight == 1)
        assert(test_font.italic is False)
