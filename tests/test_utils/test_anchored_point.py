import unittest

import pytest

from brown.utils.anchored_point import AnchoredPoint
from brown.utils.point import Point
from brown.utils.units import Unit


class TestAnchoredPoint(unittest.TestCase):

    def setUp(self):
        # Any object will do for anchored point parents under test
        self.test_parent = 'mock parent'

    def test_init(self):
        test_point = AnchoredPoint(5, 6, self.test_parent)
        assert(test_point.x == 5)
        assert(test_point.y == 6)
        assert(test_point.parent == self.test_parent)

    def test_from_existing(self):
        original = AnchoredPoint(5, 6, self.test_parent)
        clone = AnchoredPoint.from_existing(original)
        # id() check may fail on non-CPython interpreters
        assert(id(original) != id(clone))
        assert(original.x == clone.x)
        assert(original.y == clone.y)
        assert(original.parent == clone.parent)

    def test_from_point(self):
        original = Point(5, 6)
        clone = AnchoredPoint.from_point(original, self.test_parent)
        # id() check may fail on non-CPython interpreters
        assert(id(original) != id(clone))
        assert(original.x == clone.x)
        assert(original.y == clone.y)
        assert(clone.parent == self.test_parent)

    def test_to_unit(self):
        test_point = AnchoredPoint(5, 6, self.test_parent).to_unit(Unit)
        assert(isinstance(test_point.x, Unit))
        assert(isinstance(test_point.y, Unit))
        assert(test_point.x == Unit(5))
        assert(test_point.y == Unit(6))
        assert(test_point.parent == self.test_parent)

    def test__eq__(self):
        test_point = AnchoredPoint(5, 6, self.test_parent)
        test_point_eq = AnchoredPoint(5, 6, self.test_parent)
        test_point_ne_1 = AnchoredPoint(1234, 6, self.test_parent)
        test_point_ne_2 = AnchoredPoint(5, 1234, self.test_parent)
        test_point_ne_3 = AnchoredPoint(5, 6, None)
        assert(test_point == test_point_eq)
        assert(test_point != test_point_ne_1)
        assert(test_point != test_point_ne_2)
        assert(test_point != test_point_ne_3)

    def test__add__(self):
        p1 = AnchoredPoint(1, 2, None)
        p2 = AnchoredPoint(3, 4, None)
        p3 = AnchoredPoint(5, 6, self.test_parent)
        p4 = AnchoredPoint(7, 8, self.test_parent)
        assert(p1 + p2 == AnchoredPoint(4, 6, None))
        assert(p3 + p4 == AnchoredPoint(12, 14, self.test_parent))
        with pytest.raises(AttributeError):
            p2 + p3
        with pytest.raises(TypeError):
            p2 + 5
        with pytest.raises(TypeError):
            p1 + Point(0, 0)

    def test__sub__(self):
        p1 = AnchoredPoint(1, 2, None)
        p2 = AnchoredPoint(3, 4, None)
        p3 = AnchoredPoint(5, 6, self.test_parent)
        p4 = AnchoredPoint(7, 8, self.test_parent)
        assert(p1 - p2 == AnchoredPoint(-2, -2, None))
        assert(p3 - p4 == AnchoredPoint(-2, -2, self.test_parent))
        with pytest.raises(AttributeError):
            p2 - p3
        with pytest.raises(TypeError):
            p2 - 5
        with pytest.raises(TypeError):
            p1 - Point(0, 0)

    def test__mult__(self):
        p1 = AnchoredPoint(1, 2, None)
        assert(p1 * -1) == AnchoredPoint(-1, -2, None)
        p2 = AnchoredPoint(Unit(2), Unit(3), None)
        assert(p2 * Unit(-1) == AnchoredPoint(Unit(-2), Unit(-3), None))
