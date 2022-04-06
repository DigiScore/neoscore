import math
import unittest

from neoscore.core.math_helpers import (
    clamp_value,
    interpolate,
    is_power_of_2,
    min_and_max,
    point_angle,
    sign,
)
from neoscore.core.point import Point
from neoscore.core.units import ZERO, Unit


class TestMathHelpers(unittest.TestCase):
    def test_linear_interp(self):
        assert interpolate(
            Point(Unit(0), Unit(0)), Point(Unit(1), Unit(1)), Unit(2)
        ) == Unit(2)
        assert interpolate(
            Point(Unit(1), Unit(1)), Point(Unit(0), Unit(0)), Unit(-1)
        ) == Unit(-1)
        assert interpolate(
            Point(Unit(0), Unit(0)), Point(Unit(2), Unit(1)), Unit(3)
        ) == Unit(1.5)

    def test_linear_interp_with_units_preserves_units(self):
        assert interpolate(
            Point(Unit(0), Unit(0)), Point(Unit(2), Unit(1)), Unit(3)
        ) == Unit(1.5)

    def test_clamp_value(self):
        assert clamp_value(-50, 3, 5) == 3
        assert clamp_value(3, 3, 5) == 3
        assert clamp_value(4, 3, 5) == 4
        assert clamp_value(5, 3, 5) == 5
        assert clamp_value(50, 3, 5) == 5

    def test_min_and_max(self):
        assert min_and_max([1, 5, 7, 8, 10]) == (1, 10)

    def test_sign(self):
        assert sign(Unit(1)) == 1
        assert sign(Unit(0)) == 1
        assert sign(Unit(-1)) == -1

    def test_is_power_of_2(self):
        assert is_power_of_2(-2) is False
        assert is_power_of_2(-1) is False
        assert is_power_of_2(0) is False
        assert is_power_of_2(1) is True
        assert is_power_of_2(2) is True
        assert is_power_of_2(4) is True
        assert is_power_of_2(8) is True

    def test_point_angle(self):
        assert point_angle(Point(ZERO, ZERO)) == 0
        assert point_angle(Point(Unit(1), ZERO)) == 0
        self.assertAlmostEqual(point_angle(Point(ZERO, Unit(1))), math.pi / 2)
        self.assertAlmostEqual(point_angle(Point(Unit(-1), Unit(1))), math.pi * 0.75)
        self.assertAlmostEqual(point_angle(Point(Unit(-1), Unit(-1))), -math.pi * 0.75)
