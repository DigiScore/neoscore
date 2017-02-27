import unittest
import os

import pytest
from PyQt5 import QtGui

from brown.config import config
from brown.core import brown
from brown.interface.font_interface import FontInterface
from brown.utils.units import Unit


class MockUnit(Unit):
    _conversion_rate = 0.5


class TestFontInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()
        test_font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        self.font_id = brown._app_interface.register_font(
            test_font_file_path)

    def test_init(self):
        test_font = FontInterface('Bravura', MockUnit(12), 1, False)
        assert(test_font.family_name == 'Bravura')
        assert(test_font.size == MockUnit(12))
        assert(test_font.weight == 1)
        assert(test_font.italic is False)

    def test_init_qt_attribute_transfer(self):
        test_font = FontInterface('Bravura', MockUnit(12), 1, False)
        assert(isinstance(test_font._qt_object, QtGui.QFont))
        assert(test_font._qt_object.bold() is False)
        assert(test_font._qt_object.italic() is False)
        assert(test_font._qt_object.pointSize() == 6)
        assert(test_font._qt_object.weight() == 1)

    @pytest.mark.skip
    # Skip this test - seems to vary by OS or display settings?
    # May not actually be a problem. Proper testing to see if this
    # is an issue will likely require visual checks on different OS's.
    def test_em_size(self):
        test_font = FontInterface('Bravura', MockUnit(2000), 1, False)
        assert(int(test_font.em_size) == 366)
