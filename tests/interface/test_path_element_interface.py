import pytest
import unittest

from brown.core import brown
from brown.utils.point import Point
from brown.interface.path_interface import PathInterface
from mock_graphic_object_interface import MockGraphicObjectInterface
from brown.interface.path_element_interface import PathElementInterface
from brown.utils.path_element_type import PathElementType


class TestPathElementInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        test_path = PathInterface((5, 6))
        test_path.line_to((10, 11))
        qt_element = test_path._qt_path.elementAt(1)
        test_element = PathElementInterface(qt_element, test_path, 1)
        assert(float(test_element.pos.x) == 10)
        assert(float(test_element.pos.y) == 11)
        assert(test_element.parent_path == test_path)
        assert(test_element.element_type == PathElementType.line_to)
        assert(test_element.index == 1)
        assert(test_element._qt_object == qt_element)

    def test_pos_setters_hook_moves_qt_line(self):
        test_path = PathInterface((5, 6))
        test_path.line_to((10, 11))
        qt_element = test_path._qt_path.elementAt(1)
        test_element = PathElementInterface(qt_element, test_path, 1)
        # Test x change
        test_element.pos.x = 100
        assert(test_path._qt_path.elementAt(1).x == 100)
        assert(test_path._qt_object.path() == test_path._qt_path)
        # Test y change
        test_element.pos.y = 101
        assert(test_path._qt_path.elementAt(1).y == 101)
        assert(test_path._qt_object.path() == test_path._qt_path)

    def test_pos_setter_updates_element_in_parent_path(self):
        test_path = PathInterface((5, 6))
        test_path.line_to((10, 11))
        qt_element = test_path._qt_path.elementAt(1)
        test_element = PathElementInterface(qt_element, test_path, 1)
        test_element.pos = Point(50, 51)
        assert(test_element.pos.x == 50)
        assert(test_element.pos.y == 51)
        # Retry test in test_pos_setters_hook_moves_qt_line to make sure
        # pos.setters_hook was correctly set
        test_element.pos.x = 100
        assert(test_path._qt_path.elementAt(1).x == 100)
        assert(test_path._qt_object.path() == test_path._qt_path)

    def test_is_move_to(self):
        test_path = PathInterface((5, 6))
        test_path.move_to((10, 11))
        qt_element = test_path._qt_path.elementAt(0)
        test_element = PathElementInterface(qt_element, test_path, 0)
        assert(test_element.element_type == PathElementType.move_to)

    def test_is_line_to(self):
        test_path = PathInterface((5, 6))
        test_path.line_to((10, 11))
        qt_element = test_path._qt_path.elementAt(1)
        test_element = PathElementInterface(qt_element, test_path, 0)
        assert(test_element.element_type == PathElementType.line_to)

    def test_curves_and_control_points(self):
        # This behavior is correct, but not yet implemented

        test_path = PathInterface((5, 6))
        test_path.cubic_to((10, 11), (20, 0), (50, 30))

        qt_element_1 = test_path._qt_path.elementAt(1)
        test_element_1 = PathElementInterface(qt_element_1, test_path, 0)
        assert(test_element_1.element_type == PathElementType.control_point)

        qt_element_2 = test_path._qt_path.elementAt(2)
        test_element_2 = PathElementInterface(qt_element_2, test_path, 0)
        assert(test_element_2.element_type == PathElementType.control_point)

        qt_element_3 = test_path._qt_path.elementAt(3)
        test_element_3 = PathElementInterface(qt_element_3, test_path, 0)
        assert(test_element_3.element_type == PathElementType.curve_to)
