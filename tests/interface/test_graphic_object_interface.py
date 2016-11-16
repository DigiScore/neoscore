import unittest

from brown.core import brown
from brown.interface.pen_interface import PenInterface
from brown.interface.brush_interface import BrushInterface
from brown.utils.point import Point
from brown.utils.graphic_unit import GraphicUnit

from mock_graphic_object_interface import MockGraphicObjectInterface


class TestGraphicObjectInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_pos_after_init(self):
        test_object = MockGraphicObjectInterface((5, 6))
        assert(test_object.pos == test_object._pos)
        assert(test_object.pos.x == GraphicUnit(5))
        assert(test_object.pos.y == GraphicUnit(6))
        assert(test_object._qt_object.x() == test_object.pos.x.value)
        assert(test_object._qt_object.y() == test_object.pos.y.value)

    def test_pos_setter_changes_qt_object(self):
        test_object = MockGraphicObjectInterface((5, 6))
        test_object.pos = (10, 11)
        assert(test_object.x == test_object.pos.x)
        assert(test_object.y == test_object.pos.y)
        assert(test_object.pos.x.value == test_object._qt_object.x())
        assert(test_object.pos.y.value == test_object._qt_object.y())

    def test_x_setter_changes_qt_object(self):
        test_object = MockGraphicObjectInterface((5, 6))
        test_object.x = 100
        assert(test_object.x == test_object._qt_object.x())

    def test_y_setter_changes_qt_object(self):
        test_object = MockGraphicObjectInterface((5, 6))
        test_object.y = 100
        assert(test_object.y == test_object._qt_object.y())

    def test_pen_after_init(self):
        test_pen = PenInterface('#eeeeee')
        test_object = MockGraphicObjectInterface((5, 6), pen=test_pen)
        assert(test_object.pen == test_object._pen)
        assert(test_object.pen == test_pen)
        assert(test_object._qt_object.pen() == test_object.pen._qt_object)

    def test_pen_setter_changes_qt_object(self):
        test_object = MockGraphicObjectInterface((5, 6), pen=None)
        test_pen = PenInterface('#eeeeee')
        test_object.pen = test_pen
        assert(test_object._qt_object.pen() == test_object.pen._qt_object)

    def test_brush_after_init(self):
        test_brush = BrushInterface('#eeeeee')
        test_object = MockGraphicObjectInterface((5, 6), brush=test_brush)
        assert(test_object.brush == test_object._brush)
        assert(test_object.brush == test_brush)
        assert(test_object._qt_object.brush() == test_object.brush._qt_object)

    def test_brush_setter_changes_qt_object(self):
        test_object = MockGraphicObjectInterface((5, 6), brush=None)
        test_brush = BrushInterface('#eeeeee')
        test_object.brush = test_brush
        assert(test_object._qt_object.brush() == test_object.brush._qt_object)

    def test_parent_after_init(self):
        test_parent = MockGraphicObjectInterface((5, 6))
        test_child = MockGraphicObjectInterface((100, 100), parent=test_parent)
        assert(test_child.parent == test_child._parent)
        assert(test_child._qt_object.parentItem() == test_child._parent._qt_object)

    def test_parent_setter_changes_qt_object(self):
        test_parent = MockGraphicObjectInterface((5, 6))
        test_child = MockGraphicObjectInterface((100, 100))
        test_child.parent = test_parent
        assert(test_child._qt_object.parentItem() == test_child._parent._qt_object)
