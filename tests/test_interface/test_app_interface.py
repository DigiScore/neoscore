import os
import unittest

from PyQt5 import QtWidgets
from PyQt5 import QtGui
import pytest

from brown.interface.app_interface import AppInterface, FontRegistrationError
from brown import config


@pytest.mark.skip
class TestAppInterface(unittest.TestCase):

    def setUp(self):
        self.interface = AppInterface()
        self.interface.create_document()

    def test_create_document(self):
        # QApplication init
        assert(isinstance(self.interface.app, QtWidgets.QApplication))
        # QGraphicsScene setup
        assert(isinstance(self.interface.scene, QtWidgets.QGraphicsScene))
        # QGraphicsView setup
        assert(isinstance(self.interface.view, QtWidgets.QGraphicsView))
        # Check that view's scene was correctly set to self.interface.scene
        assert(self.interface.view.scene() == self.interface.scene)
        # Check that render hints were passed correctly
        # (Use a bitwise AND mask to check for the set flag
        # because Qt stores flags by bitwise OR-ing them)
        assert(int(self.interface.view.renderHints() & QtGui.QPainter.Antialiasing))

    @pytest.mark.skip
    def test_show(self):
        # TODO: How to test this?
        pass

    @pytest.mark.skip
    def test_destroy(self):
        # TODO: How to test this?
        pass

    def test_register_font(self):
        test_font_file_path = os.path.join(config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        font_id = AppInterface.register_font(test_font_file_path)
        assert(QtGui.QFontDatabase.applicationFontFamilies(font_id) == ['Bravura'])

    def test_register_font_with_invalid_path(self):
        test_font_file_path = "path that doesn't exist"
        with pytest.raises(FontRegistrationError):
            AppInterface.register_font(test_font_file_path)
