from neoscore.utils.math_helpers import (
    clamp_value,
    interpolate,
    is_power_of_2,
    min_and_max,
    sign,
)
from neoscore.utils.point import Point
from neoscore.utils.units import Unit


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


def test_is_power_of_2():
    assert is_power_of_2(-2) is False
    assert is_power_of_2(-1) is False
    assert is_power_of_2(0) is False
    assert is_power_of_2(1) is True
    assert is_power_of_2(2) is True
    assert is_power_of_2(4) is True
    assert is_power_of_2(8) is True
