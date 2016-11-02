import unittest

from PyQt5 import QtWidgets

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

    def test_x_after_init(self):
        test_object = MockSubclass1(None, 5, 6)
        assert(test_object.x == test_object._x)
        assert(test_object.x == 5)
        assert(test_object._qt_object.x() == test_object.x)

    def test_x_setter_changes_qt_object(self):
        test_object = MockSubclass1(None, 5, 6)
        test_object.x = 100
        assert(test_object.x == test_object._qt_object.x())

    def test_y_after_init(self):
        test_object = MockSubclass1(None, 5, 6)
        assert(test_object.y == 6)
        assert(test_object.y == test_object._y)
        assert(test_object._qt_object.y() == test_object.y)

    def test_y_setter_changes_qt_object(self):
        test_object = MockSubclass1(None, 5, 6)
        test_object.y = 100
        assert(test_object.y == test_object._qt_object.y())

    def test_pen_after_init(self):
        test_pen = PenInterface('eeeeee')
        test_object = MockSubclass1(None, 5, 6, pen=test_pen)
        assert(test_object.pen == test_object._pen)
        assert(test_object.pen == test_pen)
        assert(test_object._qt_object.pen() == test_object.pen._qt_object)

    def test_pen_setter_changes_qt_object(self):
        test_object = MockSubclass1(None, 5, 6, pen=None)
        test_pen = PenInterface('eeeeee')
        test_object.pen = test_pen
        assert(test_object._qt_object.pen() == test_object.pen._qt_object)

    def test_brush_after_init(self):
        test_brush = BrushInterface('eeeeee')
        test_object = MockSubclass1(None, 5, 6, brush=test_brush)
        assert(test_object.brush == test_object._brush)
        assert(test_object.brush == test_brush)
        assert(test_object._qt_object.brush() == test_object.brush._qt_object)

    def test_brush_setter_changes_qt_object(self):
        test_object = MockSubclass1(None, 5, 6, brush=None)
        test_brush = BrushInterface('eeeeee')
        test_object.brush = test_brush
        assert(test_object._qt_object.brush() == test_object.brush._qt_object)

    def test_parent_after_init(self):
        test_parent = MockSubclass1(None, 5, 6)
        test_child = MockSubclass1(test_parent, 100, 100)
        assert(test_child.parent == test_child._parent)
        assert(test_child._qt_object.parentItem() == test_child._parent._qt_object)

    def test_parent_setter_changes_qt_object(self):
        test_parent = MockSubclass1(None, 5, 6)
        test_child = MockSubclass1(None, 100, 100)
        test_child.parent = test_parent
        assert(test_child._qt_object.parentItem() == test_child._parent._qt_object)
