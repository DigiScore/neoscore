import unittest
import pytest

from brown.utils.point import Point


class TestPoint(unittest.TestCase):

    def test_init_with_pair(self):
        test_point = Point(5, 6)
        assert(test_point.x == 5)
        assert(test_point.y == 6)

    def test_init_with_2_tuple(self):
        test_point = Point((5, 6))
        assert(test_point.x == 5)
        assert(test_point.y == 6)

    def test_init_with_existing_Point(self):
        existing_point = Point(5, 6)
        test_point = Point(existing_point)
        assert(test_point.x == 5)
        assert(test_point.y == 6)

    def test_iteration(self):
        test_point = Point(5, 6)
        result = []
        for dimension in test_point:
            result.append(dimension)
        assert(result == [5, 6])

    def test_indexing(self):
        test_point = Point(5, 6)
        assert(test_point[0] == 5)
        assert(test_point[1] == 6)

    def test_indexing_with_invalid_raises_IndexError(self):
        test_point = Point(5, 6)
        with pytest.raises(IndexError):
            test_point[3]
        with pytest.raises(IndexError):
            test_point[-1]
        with pytest.raises(TypeError):
            test_point['nonsense index']
