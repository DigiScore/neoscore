import unittest

from brown.core import brown
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
        test_object = PathInterface((5, 6), test_pen, test_brush, mock_parent)
        assert(test_object.x == 5)
        assert(test_object._qt_object.x() == 5)
        assert(test_object.y == 6)
        assert(test_object._qt_object.y() == 6)
        assert(test_object.parent == mock_parent)
        assert(test_object._qt_object.parentItem() == test_object.parent._qt_object)
        assert(test_object.brush == test_brush)
        assert(test_object._qt_object.brush() == test_brush._qt_object)
        assert(test_object.pen == test_pen)
        assert(test_object._qt_object.pen() == test_pen._qt_object)
        assert(test_object.current_path_position.x == 0)
        assert(test_object.current_path_position.y == 0)

    def test_current_path_x(self):
        test_object = PathInterface((5, 6))
        assert(test_object.current_path_x == test_object.current_path_position.x)

    def test_current_path_y(self):
        test_object = PathInterface((5, 6))
        assert(test_object.current_path_y == test_object.current_path_position.y)

    def test_line_to(self):
        test_object = PathInterface((5, 6))
        test_object.line_to(10, 12)
        assert(test_object.current_path_position.x == 10)
        assert(test_object.current_path_position.y == 12)
        assert(test_object._qt_path.currentPosition().x() == 10)
        assert(test_object._qt_path.currentPosition().y() == 12)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_cubic_to(self):
        test_object = PathInterface((5, 6))
        test_object.cubic_to((10, 11),
                             (0, 1),
                             (5, 6))
        assert(test_object.current_path_position.x == 5)
        assert(test_object.current_path_position.y == 6)
        assert(test_object._qt_path.currentPosition().x() == 5)
        assert(test_object._qt_path.currentPosition().y() == 6)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_move_to(self):
        test_object = PathInterface((5, 6))
        test_object.move_to(10, 11)
        assert(test_object.current_path_position.x == 10)
        assert(test_object.current_path_position.y == 11)
        assert(test_object._qt_path.currentPosition().x() == 10)
        assert(test_object._qt_path.currentPosition().y() == 11)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_close_subpath(self):
        test_object = PathInterface((5, 6))
        test_object.close_subpath()
        assert(test_object.current_path_position.x == 0)
        assert(test_object.current_path_position.y == 0)
        assert(test_object._qt_path.currentPosition().x() == 0)
        assert(test_object._qt_path.currentPosition().y() == 0)
        # TODO: Actually inspect contents of path and make sure they
        #       are as expected

    def test_element_at(self):
        test_object = PathInterface((5, 6))
        test_object.line_to((10, 11))
        last_element = test_object.element_at(-1)
        assert(float(last_element.pos.x) == 10)
        assert(float(last_element.pos.y) == 11)
        assert(last_element.is_line_to is True)
        assert(last_element.is_move_to is False)
        assert(last_element.is_curve_to is False)
