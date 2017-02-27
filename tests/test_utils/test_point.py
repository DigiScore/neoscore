import unittest
from nose.tools import assert_raises

from brown.utils.units import Unit, Mm
from brown.utils.point import Point


class TestPoint(unittest.TestCase):

    def test_init(self):
        test_point = Point(5, 6, -1)
        assert(test_point.x == 5)
        assert(test_point.y == 6)
        assert(test_point.page == -1)

    def test_page_defaults_to_0(self):
        test_point = Point(1, 2)
        assert(test_point.page == 0)

    def test_from_existing(self):
        original = Point(5, 6, 2)
        clone = Point.from_existing(original)
        # NOTE: id() check may fail on non-CPython interpreters
        assert(id(original) != id(clone))
        assert(original.x == clone.x)
        assert(original.y == clone.y)
        assert(original.page == clone.page)

    def test_to_unit_from_int(self):
        test_point = Point(5, 6, 2)
        returned_value = test_point.to_unit(Unit)
        assert(test_point == returned_value)
        assert(isinstance(test_point.x, Unit))
        assert(isinstance(test_point.y, Unit))
        assert(test_point.x == Unit(5))
        assert(test_point.y == Unit(6))
        assert(test_point.page == 2)

    def test_to_unit_from_other_unit(self):
        test_point = Point(Unit(1), Unit(2), 2)
        test_point.to_unit(Mm)
        assert(isinstance(test_point.x, Mm))
        assert(isinstance(test_point.y, Mm))
        self.assertAlmostEqual(test_point.x, Mm(Unit(1)))
        self.assertAlmostEqual(test_point.y, Mm(Unit(2)))
        assert(test_point.page == 2)

    def test__hash__(self):
        assert({Point(1, 2), Point(1, 2), Point(3, 4), Point(3, 4, 2)} ==
               {Point(1, 2), Point(3, 4), Point(3, 4, 2)})

    def test__eq__(self):
        p1 = Point(5, 6)
        p2 = Point(5, 6)
        p3 = Point(5, 7)
        p4 = Point(5, 7, 1)
        p5 = Point(5, 7, 1)
        assert(p1 == p2)
        assert(p1 != p3)
        assert(p1 != (5, 6))
        assert(p3 != p4)
        assert(p4 == p5)

    def test__add__(self):
        p1 = Point(1, 2, 7)
        p2 = Point(3, 4, 8)
        assert(p1 + p2 == Point(4, 6, 15))
        with assert_raises(TypeError):
            p1 + 1

    def test__sub__(self):
        p1 = Point(1, 2, 7)
        p2 = Point(3, 4, 8)
        assert(p1 - p2 == Point(-2, -2, -1))
        with assert_raises(TypeError):
            p1 - 1

    def test__mul__(self):
        p1 = Point(1, 2, 7)
        assert(p1 * -1) == Point(-1, -2, 7)
        p2 = Point(Unit(2), Unit(3), 7)
        assert(p2 * Unit(-1) == Point(Unit(-2), Unit(-3), 7))

    def test__abs__(self):
        assert(abs(Point(-2, -3, -4)) == Point(2, 3, 4))

    def test__round__(self):
        assert(round(Point(1.05, -3.03, 7)) == Point(1, -3, 7))
