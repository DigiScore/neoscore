import pytest
import unittest

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.interface.app_interface import AppInterface


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
