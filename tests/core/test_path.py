import pytest
import unittest

from brown.core import brown
from brown.core.path import Path
from brown.utils.point import Point
from brown.core.pen import Pen
from brown.core.brush import Brush
from brown.utils.graphic_unit import GraphicUnit
from mock_graphic_object import MockGraphicObject


class TestPath(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = MockGraphicObject((0, 0), parent=None)
        test_pen = Pen('#eeeeee')
        test_brush = Brush('#dddddd')
        test_path = Path((5, 6), test_pen, test_brush, mock_parent)
        assert(isinstance(test_path.pos, Point))
        assert(test_path.x == 5)
        assert(test_path._interface.x == 5)
        assert(test_path.y == 6)
        assert(test_path._interface.y == 6)
        assert(isinstance(test_path.current_path_position, Point))
        assert(isinstance(test_path._interface.current_path_position, Point))
        assert(test_path.current_path_x == 0)
        assert(test_path._interface.current_path_x == 0)
        assert(test_path.current_path_y == 0)
        assert(test_path._interface.current_path_y == 0)
        assert(test_path.pen == test_pen)
        assert(test_path._interface.pen == test_pen._interface)
        assert(test_path.brush == test_brush)
        assert(test_path._interface.brush == test_brush._interface)

    def test_straight_line(self):
        test_line = Path.straight_line((5, 6), (10, 11))
        assert(isinstance(test_line.pos, Point))
        assert(test_line.x == 5)
        assert(test_line.y == 6)
        assert(test_line.current_path_x == 10)
        assert(test_line.current_path_y == 11)
        assert(test_line._interface.current_path_x == 10)
        assert(test_line._interface.current_path_y == 11)

    def test_current_path_pos_has_no_setter(self):
        test_line = Path((0, 0))
        with pytest.raises(AttributeError):
            test_line.current_path_position = (7, 8)

    def test_line_to(self):
        test_path = Path((5, 6))
        test_path.line_to(10, 12)
        assert(test_path.current_path_position.x == 10)
        assert(test_path.current_path_position.y == 12)
        assert(test_path._interface.current_path_position.x == 10)
        assert(test_path._interface.current_path_position.y == 12)

    def test_cubic_to(self):
        test_path = Path((5, 6))
        test_path.cubic_to((10, 11),
                           (0, 1),
                           (5, 6))
        assert(test_path.current_path_position.x == 5)
        assert(test_path.current_path_position.y == 6)
        assert(test_path._interface.current_path_position.x == 5)
        assert(test_path._interface.current_path_position.y == 6)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_move_to(self):
        test_path = Path((5, 6))
        test_path.move_to(10, 11)
        assert(test_path.current_path_position.x == 10)
        assert(test_path.current_path_position.y == 11)
        assert(test_path._interface.current_path_position.x == 10)
        assert(test_path._interface.current_path_position.y == 11)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_close_subpath(self):
        test_path = Path((5, 6))
        test_path.close_subpath()
        assert(test_path.current_path_position.x == 0)
        assert(test_path.current_path_position.y == 0)
        assert(test_path._interface.current_path_position.x == 0)
        assert(test_path._interface.current_path_position.y == 0)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected
