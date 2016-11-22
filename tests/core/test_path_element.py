import unittest

from brown.core import brown
from brown.utils.point import Point
from brown.utils.units import Mm
from brown.core.path import Path
from brown.core.path_element import PathElement
from mock_graphic_object import MockGraphicObject


class TestPathElement(unittest.TestCase):

    def setUp(self):
        brown.setup()

    # TODO: Test me!!!!

    def test_init(self):
        test_path = Path((5, 6))
        test_path.line_to((10, 11))
        test_path_element_interface = test_path.elements[-1]
        test_element = PathElement(test_path_element_interface, test_path, test_path)
        assert(float(test_element.pos.x) == 10)
        assert(float(test_element.pos.y) == 11)
        assert(test_element.parent_path == test_path)

    def test_pos_setter_moves_path_element_in_path(self):
        test_path = Path((5, 6))
        test_path.line_to((10, 11))
        test_element = test_path.elements[-1]
        test_element.pos.x = 100
        assert(test_path.elements[-1].x == 100)
        test_element.pos.y = 101
        assert(test_path.elements[-1].y == 101)
