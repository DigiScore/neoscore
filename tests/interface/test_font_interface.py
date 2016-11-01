import pytest
import unittest
import os

from PyQt5 import QtGui

from brown.config import config
from brown.core import brown
from brown.interface.app_interface import AppInterface
from brown.interface.font_interface import FontInterface


class TestFontInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        test_font_file_path = os.path.join(config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        font_id = brown._app_interface.register_font(test_font_file_path)
        test_font = FontInterface('Bravura', 12, 1, False)
        assert(test_font.family_name == 'Bravura')
        assert(test_font.size == 12)
        assert(test_font.weight == 1)
        assert(test_font.italic is False)

    def test_init_qt_attribute_transfer(self):
        test_font_file_path = os.path.join(config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        font_id = brown._app_interface.register_font(test_font_file_path)
        test_font = FontInterface('Bravura', 12, 1, False)
        assert(isinstance(test_font._qt_object, QtGui.QFont))
        assert(test_font._qt_object.bold() is False)
        assert(test_font._qt_object.italic() is False)
        assert(test_font._qt_object.pointSize() == 12)
        assert(test_font._qt_object.weight() == 1)

    def test_qt_font_metrics_object(self):
        test_font_file_path = os.path.join(config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        font_id = brown._app_interface.register_font(test_font_file_path)
        test_font = FontInterface('Bravura', 12, 1, False)
        assert(isinstance(test_font._qt_font_metrics_object, QtGui.QFontMetricsF))
        # TODO: Revisit me once fonts and smufl get more attention
