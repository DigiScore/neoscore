import unittest

from brown.core import brown
from brown.core.path import Path
from brown.core.path_element import PathElement
from brown.core.path_element_type import PathElementType
from brown.utils.point import Point


class TestPathElement(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def test_init(self):
        test_path = Path((5, 6))
        test_element = PathElement((10, 11), PathElementType.move_to, test_path)
        assert test_element.pos == Point(10, 11)
        assert test_element.element_type == PathElementType.move_to
        assert test_element.parent_path == test_path

    def test_passing_element_type_as_int(self):
        # Test that element_type can be passed as an int
        # and be converted to its PathElementType enum equivalent
        test_path = Path((5, 6))
        test_element = PathElement((10, 11), 0, test_path)
        assert test_element.element_type == PathElementType.move_to
