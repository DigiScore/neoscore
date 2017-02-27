from nose.tools import assert_raises
import unittest

from brown.core import brown
from brown.core.path import Path
from brown.utils.path_element_type import PathElementType
from brown.utils.point import Point
from brown.core.pen import Pen
from brown.core.brush import Brush
from mock_graphic_object import MockGraphicObject


class TestPath(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = MockGraphicObject((0, 0), parent=None)
        test_pen = Pen('#eeeeee')
        test_brush = Brush('#dddddd')
        path = Path((5, 6), test_pen, test_brush, mock_parent)
        assert(isinstance(path.pos, Point))
        assert(path.x == 5)
        assert(path.y == 6)
        assert(isinstance(path.current_path_position, Point))
        assert(path.current_path_x == 0)
        assert(path.current_path_y == 0)
        assert(path.pen == test_pen)
        assert(path.brush == test_brush)

    def test_straight_line(self):
        test_line = Path.straight_line((5, 6), (10, 11))
        assert(isinstance(test_line.pos, Point))
        assert(test_line.x == 5)
        assert(test_line.y == 6)
        assert(test_line.current_path_x == 10)
        assert(test_line.current_path_y == 11)

    def test_current_path_pos_has_no_setter(self):
        test_line = Path((0, 0))
        with assert_raises(AttributeError):
            test_line.current_path_position = (7, 8)

    def test_line_to(self):
        path = Path((5, 6))
        path.line_to(10, 12)
        assert(len(path.elements) == 2)
        assert(path.elements[-1].pos.x == 10)
        assert(path.current_path_position.x == 10)
        assert(path.current_path_position.y == 12)

    def test_line_to_with_parent(self):
        path = Path((5, 6))
        parent = MockGraphicObject((100, 50))
        path.line_to(1, 3, 0, parent)
        assert(path.elements[-1].parent == parent)

    def test_cubic_to_with_no_parents(self):
        path = Path((5, 6))
        path.cubic_to((10, 11), (0, 1), (5, 6))
        assert(len(path.elements) == 4)
        assert(path.elements[0].element_type == PathElementType.move_to)
        assert(path.elements[0].pos == Point(0, 0))
        assert(path.elements[1].element_type == PathElementType.control_point)
        assert(path.elements[1].pos == Point(10, 11))
        assert(path.elements[2].element_type == PathElementType.control_point)
        assert(path.elements[2].pos == Point(0, 1))
        assert(path.elements[3].element_type == PathElementType.curve_to)
        assert(path.elements[3].pos == Point(5, 6))
        assert(path.current_path_position.x == 5)
        assert(path.current_path_position.y == 6)

    def test_cubic_to_with_parents(self):
        path = Path((0, 0))
        parent = MockGraphicObject((100, 50))
        path.cubic_to((10, 11, 0, parent), (0, 1, 0, parent), (5, 6, 0, parent))
        assert(len(path.elements) == 4)
        assert(path.elements[0].element_type == PathElementType.move_to)
        assert(path.elements[0].pos == Point(0, 0))
        assert(path.elements[1].element_type == PathElementType.control_point)
        assert(path.elements[1].pos == Point(10, 11))
        assert(path.elements[1].parent == parent)
        assert(path.elements[2].element_type == PathElementType.control_point)
        assert(path.elements[2].pos == Point(0, 1))
        assert(path.elements[2].parent == parent)
        assert(path.elements[3].element_type == PathElementType.curve_to)
        assert(path.elements[3].pos == Point(5, 6))
        assert(path.elements[3].parent == parent)
        assert(path.current_path_position.x == 105)
        assert(path.current_path_position.y == 56)

    def test_move_to_with_no_parent(self):
        path = Path((5, 6))
        path.move_to(10, 11)
        assert(len(path.elements) == 1)
        assert(path.elements[0].element_type == PathElementType.move_to)
        assert(path.elements[0].pos == Point(10, 11))
        assert(path.current_path_position.x == 10)
        assert(path.current_path_position.y == 11)

    def test_move_to_with_parent(self):
        path = Path((0, 0))
        parent = MockGraphicObject((100, 50))
        path.move_to(10, 11, 1, parent)
        assert(len(path.elements) == 1)
        assert(path.elements[0].element_type == PathElementType.move_to)
        assert(path.elements[0].pos == Point(10, 11, 1))
        assert(path.elements[0].parent == parent)
        assert(path.current_path_position.x == 110)
        assert(path.current_path_position.y == 61)
        assert(path.current_path_position.page == 1)

    def test_close_subpath(self):
        path = Path((5, 6))
        path.line_to(10, 10)
        path.line_to(10, 100)
        path.close_subpath()
        assert(len(path.elements) == 4)
        assert(path.elements[3].element_type == PathElementType.move_to)
        assert(path.elements[3].pos == Point(0, 0))
        assert(path.current_path_position.x == 0)
        assert(path.current_path_position.y == 0)
