from brown.utils.units import Unit
from brown.utils.point import Point
from brown.utils.math_helpers import linear_interp


def test_linear_interp():
    assert(linear_interp((0, 0), (1, 1), 2) == 2)
    assert(linear_interp((1, 1), (0, 0), -1) == -1)
    assert(linear_interp((0, 0), (2, 1), 3) == 1.5)


def test_linear_interp_with_points():
    assert(linear_interp(Point(0, 0), Point(1, 1), 2) == 2)


def test_linear_interp_with_units_preserves_units():
    assert(linear_interp(
        (Unit(0), Unit(0)),
        (Unit(2), Unit(1)),
        Unit(3)
        ) == Unit(1.5))
