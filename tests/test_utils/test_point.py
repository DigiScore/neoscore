import unittest

import pytest

from brown.utils.parent_point import ParentPoint
from brown.utils.point import Point
from brown.utils.units import GraphicUnit, Meter, Mm, Unit


class TestPoint(unittest.TestCase):
    def test_init(self):
        test_point = Point(Mm(5), Mm(6))
        assert test_point.x == Mm(5)
        assert test_point.y == Mm(6)

    def test_init_with_numbers_converts_to_graphic_unit(self):
        test_point = Point(5, 6)
        assert test_point.x == GraphicUnit(5)
        assert test_point.y == GraphicUnit(6)

    def test_from_existing(self):
        original = Point(5, 6)
        clone = Point.from_existing(original)
        # NOTE: id() check may fail on non-CPython interpreters
        assert id(original) != id(clone)
        assert original.x == clone.x
        assert original.y == clone.y

    def test_from_parent_point(self):
        original = ParentPoint(5, 6, "mock parent")
        clone = Point.from_existing(original)
        # NOTE: id() check may fail on non-CPython interpreters
        assert id(original) != id(clone)
        assert original.x == clone.x
        assert original.y == clone.y

    def test__hash__(self):
        assert {Point(1, 2), Point(1, 2), Point(3, 4)} == {Point(1, 2), Point(3, 4)}
        assert {Point(1, 2), Point(1, 2), Point(3, 4)} == {Point(1, 2), Point(3, 4)}
        assert {Point(Mm(1000), GraphicUnit(0)), Point(Meter(1), GraphicUnit(0))} == {
            Point(Mm(1000), GraphicUnit(0))
        }

    def test__eq__(self):
        p1 = Point(5, 6)
        p2 = Point(Unit(5), Unit(6))
        p3 = Point(5, 1234)
        p4 = Point(1234, 6)
        assert p1 == p2
        assert p1 != p3
        assert p1 != p4

    def test__add__(self):
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        assert p1 + p2 == Point(4, 6)
        with pytest.raises(TypeError):
            p1 + 1
            p1 + ParentPoint(0, 0, "mock parent")

    def test__sub__(self):
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        assert p1 - p2 == Point(-2, -2)
        with pytest.raises(TypeError):
            p1 - 1
            p1 - ParentPoint(0, 0, "mock parent")

    def test__mul__(self):
        p = Point(1, 2)
        assert p * -1 == Point(-1, -2)

    def test__abs__(self):
        assert abs(Point(-2, -3)) == Point(2, 3)
