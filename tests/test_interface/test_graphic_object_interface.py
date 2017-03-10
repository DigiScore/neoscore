import unittest

from PyQt5.QtCore import QPointF

from brown.core import brown
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.pen_interface import PenInterface
from brown.interface.brush_interface import BrushInterface
from brown.interface.qt_to_util import point_to_qt_point_f
from brown.utils.point import Point
from brown.utils.units import GraphicUnit
from brown.utils.color import Color
from brown.core.stroke_pattern import StrokePattern

from tests.mocks.mock_graphic_object_interface import MockGraphicObjectInterface


class TestGraphicObjectInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_map_to_qt_canvas_on_first_page(self):
        expected = point_to_qt_point_f(
            brown.document._map_to_canvas(
                Point(GraphicUnit(10), GraphicUnit(11), 0)))
        actual = GraphicObjectInterface._map_to_qt_canvas(
            Point(GraphicUnit(10), GraphicUnit(11)))
        self.assertAlmostEqual(expected.x(), actual.x())
        self.assertAlmostEqual(expected.y(), actual.y())

    def test_map_to_qt_canvas_on_second_page(self):
        expected = point_to_qt_point_f(
            brown.document._map_to_canvas(
                Point(GraphicUnit(10), GraphicUnit(11), 1)))
        actual = GraphicObjectInterface._map_to_qt_canvas(
            Point(GraphicUnit(10), GraphicUnit(11), 1))
        self.assertAlmostEqual(expected.x(), actual.x())
        self.assertAlmostEqual(expected.y(), actual.y())

    def test_interface_properties_after_init(self):
        grob = MockGraphicObjectInterface((GraphicUnit(5), GraphicUnit(6)))
        assert(grob.pos == Point(GraphicUnit(5), GraphicUnit(6)))

    def test_qt_pos_after_init(self):
        expected = point_to_qt_point_f(
            brown.document._map_to_canvas(
                Point(GraphicUnit(5), GraphicUnit(6), 0)))
        grob = MockGraphicObjectInterface((GraphicUnit(5), GraphicUnit(6)))
        self.assertAlmostEqual(expected.x(), grob._qt_object.x())
        self.assertAlmostEqual(expected.y(), grob._qt_object.y())

    def test_pos_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((GraphicUnit(0), GraphicUnit(0)))
        grob.pos = (GraphicUnit(10), GraphicUnit(11))
        expected = point_to_qt_point_f(
            brown.document._map_to_canvas(
                Point(GraphicUnit(10), GraphicUnit(11), 0)))
        assert(grob.x == grob.pos.x)
        assert(grob.y == grob.pos.y)
        self.assertAlmostEqual(expected.x(), grob._qt_object.x())
        self.assertAlmostEqual(expected.y(), grob._qt_object.y())

    def test_x_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((GraphicUnit(5), GraphicUnit(6)))
        grob.x = GraphicUnit(100)
        expected = point_to_qt_point_f(
            brown.document._map_to_canvas(
                Point(GraphicUnit(100), GraphicUnit(6), 0)))
        self.assertAlmostEqual(expected.x(), grob._qt_object.x())
        self.assertAlmostEqual(expected.y(), grob._qt_object.y())

    def test_y_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((GraphicUnit(5), GraphicUnit(6)))
        grob.y = GraphicUnit(100)
        expected = point_to_qt_point_f(
            brown.document._map_to_canvas(
                Point(GraphicUnit(5), GraphicUnit(100), 0)))
        self.assertAlmostEqual(expected.x(), grob._qt_object.x())
        self.assertAlmostEqual(expected.y(), grob._qt_object.y())

    def test_pen_after_init(self):
        pen = PenInterface(Color('#eeeeee'), 0, StrokePattern(1))
        grob = MockGraphicObjectInterface((5, 6), pen=pen)
        assert(grob.pen == grob._pen)
        assert(grob.pen == pen)
        assert(grob._qt_object.pen() == grob.pen._qt_object)

    def test_pen_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((5, 6), pen=None)
        pen = PenInterface(Color('#eeeeee'), 0, StrokePattern(1))
        grob.pen = pen
        assert(grob._qt_object.pen() == grob.pen._qt_object)

    def test_brush_after_init(self):
        brush = BrushInterface(Color('#eeeeee'))
        grob = MockGraphicObjectInterface((5, 6), brush=brush)
        assert(grob.brush == grob._brush)
        assert(grob.brush == brush)
        assert(grob._qt_object.brush() == grob.brush._qt_object)

    def test_brush_setter_changes_qt_object(self):
        grob = MockGraphicObjectInterface((5, 6), brush=None)
        brush = BrushInterface(Color('#eeeeee'))
        grob.brush = brush
        assert(grob._qt_object.brush() == grob.brush._qt_object)
