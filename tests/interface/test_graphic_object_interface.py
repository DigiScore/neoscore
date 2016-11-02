import unittest
import pytest


from PyQt5 import QtWidgets
from PyQt5 import QtGui

from brown.core import brown
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.pen_interface import PenInterface
from brown.interface.brush_interface import BrushInterface


"""

Test the partly-abstract GraphicObjectInterface with a dummy subclass
ensuring the implemented functionality is working correctly.

"""


class MockSubclass1(GraphicObjectInterface):

    """Only need to implement init for a functional mock subclass"""

    def __init__(self, parent, x, y, pen=None, brush=None):
        self._qt_object = QtWidgets.QGraphicsRectItem(x, y, 10, 10)
        self.x = x
        self.y = y
        self.parent = parent
        self.pen = pen
        self.brush = brush


class TestGraphicObjectInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_x_getter(self):
        test_object = MockSubclass1(None, 5, 6)
        assert(test_object.x == test_object._x)

    def test_x_setter(self):
        test_object = MockSubclass1(None, 5, 6)
        assert(test_object.x == 5)

    def test_y_getter(self):
        test_object = MockSubclass1(None, 5, 6)
        assert(test_object.y == test_object._y)

    def test_y_setter(self):
        test_object = MockSubclass1(None, 5, 6)
        assert(test_object.y == 6)

    def test_pen_getter(self):
        test_object = MockSubclass1(None, 5, 6)
        assert(test_object.pen == test_object._pen)

    def test_pen_setter(self):
        test_pen = PenInterface('eeeeee')
        test_object = MockSubclass1(None, 5, 6, pen=test_pen)
        assert(test_object.pen == test_pen)

    def test_brush_getter(self):
        test_object = MockSubclass1(None, 5, 6)
        assert(test_object.brush == test_object._brush)

    def test_brush_setter(self):
        test_brush = BrushInterface('eeeeee')
        test_object = MockSubclass1(None, 5, 6, brush=test_brush)
        assert(test_object.brush == test_brush)

    @pytest.mark.skip
    def test_parent_getter(self):
        # TODO
        pass

    # TODO: More tests, make tests less tautological. Especially do lots
    #       of testing that setters actually propagate changes to underlying
    #       _qt_objects
