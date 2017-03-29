import unittest

from brown.core import brown
from brown.utils.point import Point
from brown.utils.path_element_type import PathElementType
from brown.utils.color import Color
from brown.core.fill_pattern import FillPattern
from brown.core.stroke_pattern import StrokePattern
from brown.interface.path_interface import PathInterface
from brown.interface.pen_interface import PenInterface
from brown.interface.brush_interface import BrushInterface


class TestPathInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.pen = PenInterface(Color('#000000'), 0, StrokePattern.SOLID)
        self.brush = BrushInterface(Color('#000000'), FillPattern.SOLID_COLOR)

    def test_init(self):
        test_path = PathInterface(Point(5, 6), self.pen, self.brush)
        assert(test_path.brush == self.brush)
        assert(test_path._qt_object.brush() == self.brush._qt_object)
        assert(test_path.pen == self.pen)
        assert(test_path._qt_object.pen() == self.pen._qt_object)
        assert(test_path.current_path_position.x == 0)
        assert(test_path.current_path_position.y == 0)

    def test_current_path_x(self):
        test_path = PathInterface(Point(5, 6), self.pen, self.brush)
        assert(test_path.current_path_x == test_path.current_path_position.x)

    def test_current_path_y(self):
        test_path = PathInterface(Point(5, 6), self.pen, self.brush)
        assert(test_path.current_path_y == test_path.current_path_position.y)

    def test_initial_element_count_is_0(self):
        test_path = PathInterface(Point(5, 6), self.pen, self.brush)
        assert(test_path._qt_path.elementCount() == 0)

    def test_line_to(self):
        test_path = PathInterface(Point(5, 6), self.pen, self.brush)
        test_path.line_to(Point(10, 12))
        assert(test_path.current_path_position.x == 10)
        assert(test_path.current_path_position.y == 12)
        assert(test_path._qt_path == test_path._qt_object.path())
        assert(test_path._qt_path.currentPosition().x() == 10)
        assert(test_path._qt_path.currentPosition().y() == 12)
        assert(test_path._qt_path.elementCount() == 2)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_cubic_to(self):
        test_path = PathInterface(Point(5, 6), self.pen, self.brush)
        test_path.cubic_to(Point(10, 11),
                           Point(0, 1),
                           Point(5, 6))
        assert(test_path.current_path_position.x == 5)
        assert(test_path.current_path_position.y == 6)
        assert(test_path._qt_path.currentPosition().x() == 5)
        assert(test_path._qt_path.currentPosition().y() == 6)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_move_to(self):
        test_path = PathInterface(Point(5, 6), self.pen, self.brush)
        test_path.move_to(Point(10, 11))
        move_to_el = test_path.element_at(0)
        assert(test_path._qt_path.elementCount() == 1)
        assert(float(move_to_el.pos.x) == 10)
        assert(float(move_to_el.pos.y) == 11)
        assert(move_to_el.parent_path == test_path)
        assert(move_to_el.element_type == PathElementType.move_to)

    def test_close_subpath(self):
        test_path = PathInterface(Point(5, 6), self.pen, self.brush)
        test_path.close_subpath()
        assert(test_path.current_path_position.x == 0)
        assert(test_path.current_path_position.y == 0)
        assert(test_path._qt_path.currentPosition().x() == 0)
        assert(test_path._qt_path.currentPosition().y() == 0)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_element_at(self):
        test_path = PathInterface(Point(5, 6), self.pen, self.brush)
        test_path.line_to(Point(10, 11))
        line_to_el = test_path.element_at(1)
        assert(float(line_to_el.pos.x) == 10)
        assert(float(line_to_el.pos.y) == 11)
        assert(line_to_el.parent_path == test_path)
        assert(line_to_el.element_type == PathElementType.line_to)

    def test_set_element_position_at(self):
        # TODO: Make me!
        pass
