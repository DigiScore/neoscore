from nose.tools import assert_raises
import unittest

from brown.core import brown
from brown.utils.path_element_type import PathElementType
from brown.interface.path_element_interface import PathElementInterface
from brown.interface.path_interface import PathInterface
from brown.interface.pen_interface import PenInterface
from brown.interface.brush_interface import BrushInterface
from mock_graphic_object_interface import MockGraphicObjectInterface


class TestPathInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = MockGraphicObjectInterface((0, 0), parent=None)
        test_pen = PenInterface('#eeeeee')
        test_brush = BrushInterface('#dddddd')
        test_path = PathInterface((5, 6), test_pen, test_brush, mock_parent)
        assert(test_path.x == 5)
        assert(test_path._qt_object.x() == 5)
        assert(test_path.y == 6)
        assert(test_path._qt_object.y() == 6)
        assert(test_path.parent == mock_parent)
        assert(test_path._qt_object.parentItem() == test_path.parent._qt_object)
        assert(test_path.brush == test_brush)
        assert(test_path._qt_object.brush() == test_brush._qt_object)
        assert(test_path.pen == test_pen)
        assert(test_path._qt_object.pen() == test_pen._qt_object)
        assert(test_path.current_path_position.x == 0)
        assert(test_path.current_path_position.y == 0)

    def test_current_path_x(self):
        test_path = PathInterface((5, 6))
        assert(test_path.current_path_x == test_path.current_path_position.x)

    def test_current_path_y(self):
        test_path = PathInterface((5, 6))
        assert(test_path.current_path_y == test_path.current_path_position.y)

    def test_initial_element_count_is_0(self):
        test_path = PathInterface((5, 6))
        assert(test_path._qt_path.elementCount() == 0)

    def test_line_to(self):
        test_path = PathInterface((5, 6))
        test_path.line_to((10, 12))
        assert(test_path.current_path_position.x == 10)
        assert(test_path.current_path_position.y == 12)
        assert(test_path._qt_path == test_path._qt_object.path())
        assert(test_path._qt_path.currentPosition().x() == 10)
        assert(test_path._qt_path.currentPosition().y() == 12)
        assert(test_path._qt_path.elementCount() == 2)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_cubic_to(self):
        test_path = PathInterface((5, 6))
        test_path.cubic_to((10, 11),
                             (0, 1),
                             (5, 6))
        assert(test_path.current_path_position.x == 5)
        assert(test_path.current_path_position.y == 6)
        assert(test_path._qt_path.currentPosition().x() == 5)
        assert(test_path._qt_path.currentPosition().y() == 6)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_move_to(self):
        test_path = PathInterface((5, 6))
        test_path.move_to((10, 11))
        move_to_el = test_path.element_at(0)
        assert(test_path._qt_path.elementCount() == 1)
        assert(float(move_to_el.pos.x) == 10)
        assert(float(move_to_el.pos.y) == 11)
        assert(move_to_el.parent_path == test_path)
        assert(move_to_el.element_type == PathElementType.move_to)

    def test_close_subpath(self):
        test_path = PathInterface((5, 6))
        test_path.close_subpath()
        assert(test_path.current_path_position.x == 0)
        assert(test_path.current_path_position.y == 0)
        assert(test_path._qt_path.currentPosition().x() == 0)
        assert(test_path._qt_path.currentPosition().y() == 0)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_element_at(self):
        test_path = PathInterface((5, 6))
        test_path.line_to((10, 11))
        line_to_el = test_path.element_at(1)
        assert(float(line_to_el.pos.x) == 10)
        assert(float(line_to_el.pos.y) == 11)
        assert(line_to_el.parent_path == test_path)
        assert(line_to_el.element_type == PathElementType.line_to)

    def test_set_element_position_at(self):
        # TODO: Make me!
        pass
