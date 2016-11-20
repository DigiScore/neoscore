import unittest

from brown.core import brown
from brown.utils.point import Point
from brown.interface.path_interface import PathInterface
from mock_graphic_object_interface import MockGraphicObjectInterface
from brown.interface.path_element_interface import PathElementInterface


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
        assert(test_element.is_line_to is True)
        assert(test_element.is_move_to is False)
        assert(test_element.is_curve_to is False)
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
