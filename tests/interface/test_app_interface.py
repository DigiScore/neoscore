import pytest
import unittest

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.interface.app_interface import AppInterface
from brown.interface.pen_interface import PenInterface
from brown.interface.brush_interface import BrushInterface


class TestAppInterface(unittest.TestCase):

    def setUp(self):
        self.interface = AppInterface()

    def test_init(self):
        assert(self.interface.app is None)
        assert(self.interface.scene is None)
        assert(self.interface.current_pen is None)
        assert(self.interface.current_brush is None)

    def test_create_document(self):
        self.interface.create_document()
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

    def test_current_pen(self):
        self.interface.create_document()
        test_pen = PenInterface('#ffffff')
        self.interface.current_pen = test_pen
        assert(self.interface.current_pen == test_pen)

    def test_current_brush(self):
        self.interface.create_document()
        test_brush = BrushInterface('#ffffff')
        self.interface.current_brush = test_brush
        assert(self.interface.current_brush == test_brush)
