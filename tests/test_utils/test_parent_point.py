import unittest

import pytest

from brown.utils.parent_point import ParentPoint
from brown.utils.point import Point
from brown.utils.units import GraphicUnit, Mm, Unit


class TestParentPoint(unittest.TestCase):
    def setUp(self):
        # Any object will do for anchored point parents under test
        self.test_parent = "mock parent"

    def test_init(self):
        test_point = ParentPoint(Unit(5), Unit(6), self.test_parent)
        assert test_point.x == GraphicUnit(5)
        assert test_point.y == GraphicUnit(6)
        assert test_point.parent == self.test_parent

    def test_from_point(self):
        original = Point(Unit(5), Unit(6))
        clone = ParentPoint.from_point(original, self.test_parent)
        # id() check may fail on non-CPython interpreters
        assert id(original) != id(clone)
        assert original.x == clone.x
        assert original.y == clone.y
        assert clone.parent == self.test_parent

    def test__eq__(self):
        test_point = ParentPoint(Unit(5), Unit(6), self.test_parent)
        test_point_eq = ParentPoint(Unit(5), Unit(6), self.test_parent)
        test_point_ne_1 = ParentPoint(Unit(1234), Unit(6), self.test_parent)
        test_point_ne_2 = ParentPoint(Unit(5), Unit(1234), self.test_parent)
        test_point_ne_3 = ParentPoint(Unit(5), Unit(6), None)
        assert test_point == test_point_eq
        assert test_point != test_point_ne_1
        assert test_point != test_point_ne_2
        assert test_point != test_point_ne_3

    def test__add__(self):
        p1 = ParentPoint(Unit(1), Unit(2), None)
        p2 = ParentPoint(Unit(3), Unit(4), None)
        p3 = ParentPoint(Unit(5), Unit(6), self.test_parent)
        p4 = ParentPoint(Unit(7), Unit(8), self.test_parent)
        assert p1 + p2 == ParentPoint(Unit(4), Unit(6), None)
        assert p3 + p4 == ParentPoint(Unit(12), Unit(14), self.test_parent)
        with pytest.raises(AttributeError):
            p2 + p3
        with pytest.raises(TypeError):
            p2 + 5
        with pytest.raises(TypeError):
            p1 + Point(Unit(0), Unit(0))

    def test__sub__(self):
        p1 = ParentPoint(Unit(1), Unit(2), None)
        p2 = ParentPoint(Unit(3), Unit(4), None)
        p3 = ParentPoint(Unit(5), Unit(6), self.test_parent)
        p4 = ParentPoint(Unit(7), Unit(8), self.test_parent)
        assert p1 - p2 == ParentPoint(Unit(-2), Unit(-2), None)
        assert p3 - p4 == ParentPoint(Unit(-2), Unit(-2), self.test_parent)
        with pytest.raises(AttributeError):
            p2 - p3
        with pytest.raises(TypeError):
            p2 - 5
        with pytest.raises(TypeError):
            p1 - Point(Unit(0), Unit(0))

    def test__mult__(self):
        p = ParentPoint(Unit(1), Unit(2), None)
        assert p * -1 == ParentPoint(Unit(-1), Unit(-2), None)

    def test_in_unit(self):
        original = ParentPoint(Unit(1), Unit(2), self.test_parent)
        converted = original.in_unit(Mm)
        assert isinstance(converted.x, Mm)
        assert isinstance(converted.y, Mm)
        assert original == converted
