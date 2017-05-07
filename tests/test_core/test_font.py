import os
import unittest

from brown import config
from brown.core import brown
from brown.core.font import Font
from brown.interface.app_interface import AppInterface


class TestFont(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.test_font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        self.font_id = brown.register_font(
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

    def test_deriving(self):
        test_font = Font('Bravura', 12, 2, False)
        deriving_family_name = Font.deriving(test_font,
                                             size=14,
                                             weight=1,
                                             italic=True)
        assert(deriving_family_name.family_name == 'Bravura')
        assert(deriving_family_name.size == 14)
        assert(deriving_family_name.weight == 1)
        assert(deriving_family_name.italic is True)

        deriving_size = Font.deriving(test_font,
                                      family_name='Cormorant Garamond',
                                      weight=1,
                                      italic=True)
        assert(deriving_size.family_name == 'Cormorant Garamond')
        assert(deriving_size.size == 12)
        assert(deriving_size.weight == 1)
        assert(deriving_size.italic is True)

        deriving_weight = Font.deriving(test_font,
                                        family_name='Cormorant Garamond',
                                        size=14,
                                        italic=True)
        assert(deriving_weight.family_name == 'Cormorant Garamond')
        assert(deriving_weight.size == 14)
        assert(deriving_weight.weight == 2)
        assert(deriving_weight.italic is True)

        deriving_italic = Font.deriving(test_font,
                                        family_name='Cormorant Garamond',
                                        size=14,
                                        weight=2)
        assert(deriving_italic.family_name == 'Cormorant Garamond')
        assert(deriving_italic.size == 14)
        assert(deriving_italic.weight == 2)
        assert(deriving_italic.italic is False)
