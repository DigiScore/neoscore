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
        grob = MockGraphicObjectInterface((5, 6))
        assert(grob.pos == grob._pos)
        assert(grob.pos.x == GraphicUnit(5))
        assert(grob.pos.y == GraphicUnit(6))
        assert(grob._qt_object.x() == grob.pos.x.value)
        assert(grob._qt_object.y() == grob.pos.y.value)

    def test_pos_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((5, 6))
        grob.pos = (10, 11)
        assert(grob.x == grob.pos.x)
        assert(grob.y == grob.pos.y)
        assert(grob.pos.x.value == grob._qt_object.x())
        assert(grob.pos.y.value == grob._qt_object.y())

    def test_x_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((5, 6))
        grob.x = 100
        assert(grob.x == grob._qt_object.x())

    def test_y_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((5, 6))
        grob.y = 100
        assert(grob.y == grob._qt_object.y())

    def test_pen_after_init(self):
        pen = PenInterface('#eeeeee')
        grob = MockGraphicObjectInterface((5, 6), pen=pen)
        assert(grob.pen == grob._pen)
        assert(grob.pen == pen)
        assert(grob._qt_object.pen() == grob.pen._qt_object)

    def test_pen_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((5, 6), pen=None)
        pen = PenInterface('#eeeeee')
        grob.pen = pen
        assert(grob._qt_object.pen() == grob.pen._qt_object)

    def test_brush_after_init(self):
        brush = BrushInterface('#eeeeee')
        grob = MockGraphicObjectInterface((5, 6), brush=brush)
        assert(grob.brush == grob._brush)
        assert(grob.brush == brush)
        assert(grob._qt_object.brush() == grob.brush._qt_object)

    def test_brush_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((5, 6), brush=None)
        brush = BrushInterface('#eeeeee')
        grob.brush = brush
        assert(grob._qt_object.brush() == grob.brush._qt_object)

    def test_parent_after_init(self):
        parent = MockGraphicObjectInterface((5, 6))
        child = MockGraphicObjectInterface((100, 100), parent=parent)
        assert(child.parent == child._parent)
        assert(child._qt_object.parentItem() == child._parent._qt_object)

    def test_parent_setter_changes_qt_object(self):
        parent = MockGraphicObjectInterface((5, 6))
        child = MockGraphicObjectInterface((100, 100))
        child.parent = parent
        assert(child._qt_object.parentItem() == child._parent._qt_object)

    def test_pos_relative_to_item(self):
        grob = MockGraphicObjectInterface((100, 100))
        other_object = MockGraphicObjectInterface((5, 6))
        relative_x, relative_y = grob.pos_relative_to_item(other_object)
        assert(relative_x.value == 95)
        assert(relative_y.value == 94)
