import unittest
import os

import pytest
from PyQt5 import QtGui

from brown import config
from brown.core import brown
from brown.interface.font_interface import FontInterface
from brown.interface.app_interface import AppInterface
from brown.utils.units import Unit


class MockUnit(Unit):
    CONVERSION_RATE = 0.5


class TestFontInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()
        brown._app_interface._remove_all_loaded_fonts()

    def test_init(self):
        test_font = FontInterface(None, 'Bravura', MockUnit(12), 1, False)
        assert(test_font.family_name == 'Bravura')
        assert(test_font.size == MockUnit(12))
        assert(test_font.weight == 1)
        assert(test_font.italic is False)

    def test_init_qt_attribute_transfer(self):
        test_font = FontInterface(None, 'Bravura', MockUnit(12), 1, False)
        assert(isinstance(test_font.qt_object, QtGui.QFont))
        assert(test_font.qt_object.bold() is False)
        assert(test_font.qt_object.italic() is False)
        assert(test_font.qt_object.pointSize() == 6)
        assert(test_font.qt_object.weight() == 1)

    @pytest.mark.skip
    # Skip this test - seems to vary by OS or display settings?
    # May not actually be a problem. Proper testing to see if this
    # is an issue will likely require visual checks on different OS's.
    def test_em_size(self):
        test_font = FontInterface(None, 'Bravura', MockUnit(2000), 1, False)
        assert(int(test_font.em_size) == 366)
