from brown.utils.math_helpers import (
    clamp_value,
    float_to_rounded_fraction_tuple,
    interpolate,
    min_and_max,
    sign,
)
from brown.utils.point import Point
from brown.utils.units import Unit


def test_linear_interp():
    assert interpolate(
        Point(Unit(0), Unit(0)), Point(Unit(1), Unit(1)), Unit(2)
    ) == Unit(2)
    assert interpolate(
        Point(Unit(1), Unit(1)), Point(Unit(0), Unit(0)), Unit(-1)
    ) == Unit(-1)
    assert interpolate(
        Point(Unit(0), Unit(0)), Point(Unit(2), Unit(1)), Unit(3)
    ) == Unit(1.5)


def test_linear_interp_with_units_preserves_units():
    assert interpolate(
        Point(Unit(0), Unit(0)), Point(Unit(2), Unit(1)), Unit(3)
    ) == Unit(1.5)


def test_clamp_value():
    assert clamp_value(-50, 3, 5) == 3
    assert clamp_value(3, 3, 5) == 3
    assert clamp_value(4, 3, 5) == 4
    assert clamp_value(5, 3, 5) == 5
    assert clamp_value(50, 3, 5) == 5


def test_min_and_max():
    assert min_and_max([1, 5, 7, 8, 10]) == (1, 10)


def test_sign():
    assert sign(Unit(1)) == 1
    assert sign(Unit(0)) == 1
    assert sign(Unit(-1)) == -1


def test_float_to_rounded_fraction():
    assert float_to_rounded_fraction_tuple(0.4, 4) == (2, 4)
