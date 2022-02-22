import unittest

from PyQt5.QtCore import QPointF

from brown.core import brown
from brown.core.brush_pattern import BrushPattern
from brown.core.pen_cap_style import PenCapStyle
from brown.core.pen_join_style import PenJoinStyle
from brown.core.pen_pattern import PenPattern
from brown.interface.brush_interface import BrushInterface
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.utils.point import Point
from brown.utils.units import GraphicUnit, Unit
from tests.mocks.mock_graphic_object_interface import MockGraphicObjectInterface


class TestGraphicObjectInterface(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def test_interface_properties_after_init(self):
        grob = MockGraphicObjectInterface((GraphicUnit(5), GraphicUnit(6)))
        assert grob.pos == Point(GraphicUnit(5), GraphicUnit(6))

    def test_qt_pos_after_init(self):
        grob = MockGraphicObjectInterface((GraphicUnit(5), GraphicUnit(6)))
        expected = QPointF(5, 6)
        self.assertAlmostEqual(expected.x(), grob.qt_object.x())
        self.assertAlmostEqual(expected.y(), grob.qt_object.y())

    def test_pos_setter_changesqt_object(self):
        grob = MockGraphicObjectInterface((GraphicUnit(0), GraphicUnit(0)))
        grob.pos = (GraphicUnit(10), GraphicUnit(11))
        expected = QPointF(10, 11)
        assert grob.x == grob.pos.x
        assert grob.y == grob.pos.y
        self.assertAlmostEqual(expected.x(), grob.qt_object.x())
        self.assertAlmostEqual(expected.y(), grob.qt_object.y())

    def test_x_setter_changesqt_object(self):
        grob = MockGraphicObjectInterface((GraphicUnit(5), GraphicUnit(6)))
        grob.x = GraphicUnit(100)
        expected = QPointF(100, 6)
        self.assertAlmostEqual(expected.x(), grob.qt_object.x())
        self.assertAlmostEqual(expected.y(), grob.qt_object.y())

    def test_y_setter_changesqt_object(self):
        grob = MockGraphicObjectInterface((GraphicUnit(5), GraphicUnit(6)))
        grob.y = GraphicUnit(100)
        expected = QPointF(5, 100)
        self.assertAlmostEqual(expected.x(), grob.qt_object.x())
        self.assertAlmostEqual(expected.y(), grob.qt_object.y())

    def test_pen_after_init(self):
        pen = PenInterface(
            Color("#eeeeee"),
            GraphicUnit(0),
            PenPattern(1),
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        grob = MockGraphicObjectInterface((Unit(5), Unit(6)), pen=pen)
        assert grob.pen == grob._pen
        assert grob.pen == pen
        assert grob.qt_object.pen() == grob.pen.qt_object

    def test_pen_setter_changesqt_object(self):
        grob = MockGraphicObjectInterface((Unit(5), Unit(6)), pen=None)
        pen = PenInterface(
            Color("#eeeeee"),
            GraphicUnit(0),
            PenPattern(1),
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        grob.pen = pen
        assert grob.qt_object.pen() == grob.pen.qt_object

    def test_brush_after_init(self):
        brush = BrushInterface(Color("#eeeeee"), BrushPattern.SOLID)
        grob = MockGraphicObjectInterface((Unit(5), Unit(6)), brush=brush)
        assert grob.brush == grob._brush
        assert grob.brush == brush
        assert grob.qt_object.brush() == grob.brush.qt_object

    def test_brush_setter_changesqt_object(self):
        grob = MockGraphicObjectInterface((Unit(5), Unit(6)), brush=None)
        brush = BrushInterface(Color("#eeeeee"), BrushPattern.SOLID)
        grob.brush = brush
        assert grob.qt_object.brush() == grob.brush.qt_object
