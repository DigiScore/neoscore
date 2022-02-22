import unittest

from brown.core import brown
from brown.core.brush_pattern import BrushPattern
from brown.core.path_element_type import PathElementType
from brown.core.pen_cap_style import PenCapStyle
from brown.core.pen_join_style import PenJoinStyle
from brown.core.pen_pattern import PenPattern
from brown.interface.brush_interface import BrushInterface
from brown.interface.path_interface import PathInterface
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.utils.point import Point
from brown.utils.units import GraphicUnit, Unit

from ..helpers import assert_almost_equal


class TestPathInterface(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.pen = PenInterface(
            Color("#000000"),
            GraphicUnit(0),
            PenPattern.SOLID,
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        self.brush = BrushInterface(Color("#000000"), BrushPattern.SOLID)

    def test_init(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        assert test_path.brush == self.brush
        assert test_path.qt_object.brush() == self.brush.qt_object
        assert test_path.pen == self.pen
        assert test_path.qt_object.pen() == self.pen.qt_object
        assert test_path.current_draw_pos.x == GraphicUnit(0)
        assert test_path.current_draw_pos.y == GraphicUnit(0)

    def test_initial_element_count_is_0(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        assert test_path.qt_path.elementCount() == 0

    def test_line_to(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        test_path.line_to(Point(Unit(10), Unit(12)))
        assert test_path.current_draw_pos == Point(GraphicUnit(10), GraphicUnit(12))
        assert test_path.qt_path == test_path.qt_object.path()
        assert test_path.qt_path.currentPosition().x() == 10
        assert test_path.qt_path.currentPosition().y() == 12
        assert test_path.qt_path.elementCount() == 2

    def test_cubic_to(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        test_path.cubic_to(
            Point(Unit(10), Unit(11)), Point(Unit(0), Unit(1)), Point(Unit(5), Unit(6))
        )
        assert test_path.current_draw_pos == Point(GraphicUnit(5), GraphicUnit(6))
        assert test_path.qt_path.currentPosition().x() == 5
        assert test_path.qt_path.currentPosition().y() == 6

    def test_move_to(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        test_path.move_to(Point(Unit(10), Unit(11)))
        move_to_el = test_path.element_at(0)
        assert test_path.qt_path.elementCount() == 1
        assert_almost_equal(move_to_el.pos, Point(Unit(10), Unit(11)))
        assert move_to_el.path_interface == test_path
        assert move_to_el.element_type == PathElementType.move_to

    def test_close_subpath(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        test_path.close_subpath()
        assert test_path.current_draw_pos == Point(Unit(0), Unit(0))
        assert test_path.qt_path.currentPosition().x() == 0
        assert test_path.qt_path.currentPosition().y() == 0

    def test_element_at(self):
        test_path = PathInterface(Point(Unit(5), Unit(6)), self.pen, self.brush)
        test_path.line_to(Point(Unit(10), Unit(11)))
        line_to_el = test_path.element_at(1)
        assert_almost_equal(line_to_el.pos, Point(Unit(10), Unit(11)))
        assert line_to_el.path_interface == test_path
        assert line_to_el.element_type == PathElementType.line_to

    def test_set_element_position_at(self):
        # TODO: Make me!
        pass
