import unittest

from brown.core import brown
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

    def test_pos_setter_moves_qt_line(self):
        test_path = PathInterface((5, 6))
        test_path.line_to((10, 11))
        qt_element = test_path._qt_path.elementAt(1)
        test_element = PathElementInterface(qt_element, test_path, 1)
        test_element.pos.x = 100
        assert(test_path._qt_path.elementAt(1).x == 100)
