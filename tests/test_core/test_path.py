import unittest

import pytest

from brown.core import brown
from brown.core.brush import Brush
from brown.core.invisible_object import InvisibleObject
from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.path_element_type import PathElementType
from brown.utils.point import Point


class TestPath(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = InvisibleObject((0, 0), parent=None)
        test_pen = Pen('#eeeeee')
        test_brush = Brush('#dddddd')
        path = Path((5, 6), test_pen, test_brush, mock_parent)
        assert(isinstance(path.pos, Point))
        assert(path.x == 5)
        assert(path.y == 6)
        assert(isinstance(path.current_draw_pos, Point))
        assert(path.current_draw_pos == Point(0, 0))
        assert(path.pen == test_pen)
        assert(path.brush == test_brush)

    def test_straight_line(self):
        test_line = Path.straight_line((5, 6), (10, 11))
        assert(isinstance(test_line.pos, Point))
        assert(test_line.x == 5)
        assert(test_line.y == 6)
        assert(test_line.current_draw_pos == Point(10, 11))

    # noinspection PyPropertyAccess
    def test_current_path_pos_has_no_setter(self):
        test_line = Path((0, 0))
        with pytest.raises(AttributeError):
            test_line.current_draw_pos = (7, 8)

    def test_line_to(self):
        path = Path((5, 6))
        path.line_to(10, 12)
        assert(len(path.elements) == 2)
        assert(path.elements[-1].pos.x == 10)
        assert(path.current_draw_pos == Point(10, 12))

    def test_line_to_with_parent(self):
        path = Path((5, 6))
        parent = InvisibleObject((100, 50))
        path.line_to(1, 3, parent)
        assert(path.elements[-1].parent == parent)

    def test_cubic_to_with_no_parents(self):
        path = Path((5, 6))
        path.cubic_to(10, 11, 0, 1, 5, 6)
        assert(len(path.elements) == 4)
        assert(path.elements[0].element_type == PathElementType.move_to)
        assert(path.elements[0].pos == Point(0, 0))
        assert(path.elements[1].element_type == PathElementType.control_point)
        assert(path.elements[1].pos == Point(10, 11))
        assert(path.elements[2].element_type == PathElementType.control_point)
        assert(path.elements[2].pos == Point(0, 1))
        assert(path.elements[3].element_type == PathElementType.curve_to)
        assert(path.elements[3].pos == Point(5, 6))
        assert(path.current_draw_pos.x == 5)
        assert(path.current_draw_pos.y == 6)

    def test_cubic_to_with_parents(self):
        path = Path((0, 0))
        parent_1 = InvisibleObject((100, 50))
        parent_2 = InvisibleObject((100, 50))
        parent_3 = InvisibleObject((100, 50))
        path.cubic_to(10, 11, 0, 1, 5, 6, parent_1, parent_2, parent_3)
        assert(len(path.elements) == 4)
        assert(path.elements[0].element_type == PathElementType.move_to)
        assert(path.elements[0].pos == Point(0, 0))
        assert(path.elements[1].element_type == PathElementType.control_point)
        assert(path.elements[1].pos == Point(10, 11))
        assert(path.elements[1].parent == parent_1)
        assert(path.elements[2].element_type == PathElementType.control_point)
        assert(path.elements[2].pos == Point(0, 1))
        assert(path.elements[2].parent == parent_2)
        assert(path.elements[3].element_type == PathElementType.curve_to)
        assert(path.elements[3].pos == Point(5, 6))
        assert(path.elements[3].parent == parent_3)
        assert(path.current_draw_pos.x == 105)
        assert(path.current_draw_pos.y == 56)

    def test_move_to_with_no_parent(self):
        path = Path((5, 6))
        path.move_to(10, 11)
        assert(len(path.elements) == 1)
        assert(path.elements[0].element_type == PathElementType.move_to)
        assert(path.elements[0].pos == Point(10, 11))
        assert(path.current_draw_pos.x == 10)
        assert(path.current_draw_pos.y == 11)

    def test_move_to_with_parent(self):
        path = Path((0, 0))
        parent = InvisibleObject((100, 50))
        path.move_to(10, 11, parent)
        assert(len(path.elements) == 1)
        assert(path.elements[0].element_type == PathElementType.move_to)
        assert(path.elements[0].pos == Point(10, 11))
        assert(path.elements[0].parent == parent)
        assert(path.current_draw_pos.x == 110)
        assert(path.current_draw_pos.y == 61)

    def test_close_subpath(self):
        path = Path((5, 6))
        path.line_to(10, 10)
        path.line_to(10, 100)
        path.close_subpath()
        assert(len(path.elements) == 4)
        assert(path.elements[3].element_type == PathElementType.move_to)
        assert(path.elements[3].pos == Point(0, 0))
        assert(path.current_draw_pos.x == 0)
        assert(path.current_draw_pos.y == 0)
