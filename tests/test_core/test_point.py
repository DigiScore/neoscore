import unittest

import pytest

from neoscore.core.point import Point
from neoscore.core.units import Mm, Unit


class TestPoint(unittest.TestCase):
    def test_init(self):
        test_point = Point(Mm(5), Mm(6))
        assert test_point.x == Mm(5)
        assert test_point.y == Mm(6)

    def test__eq__(self):
        p1 = Point(Unit(5), Unit(6))
        p2 = Point(Unit(5), Unit(6))
        p3 = Point(Unit(5), Unit(1234))
        p4 = Point(Unit(1234), Unit(6))
        assert p1 == p2
        assert p1 != p3
        assert p1 != p4

    def test__add__(self):
        p1 = Point(Unit(1), Unit(2))
        p2 = Point(Unit(3), Unit(4))
        assert p1 + p2 == Point(Unit(4), Unit(6))
        with pytest.raises(TypeError):
            p1 + 1  # noqa

    def test__sub__(self):
        p1 = Point(Unit(1), Unit(2))
        p2 = Point(Unit(3), Unit(4))
        assert p1 - p2 == Point(Unit(-2), Unit(-2))
        with pytest.raises(TypeError):
            p1 - 1  # noqa

    def test__mul__(self):
        p = Point(Unit(1), Unit(2))
        assert p * -1 == Point(Unit(-1), Unit(-2))

    def test__abs__(self):
        assert abs(Point(Unit(-2), Unit(-3))) == Point(Unit(2), Unit(3))

    def test__neg__(self):
        assert -Point(Unit(1), Unit(-2)) == Point(Unit(-1), Unit(2))
