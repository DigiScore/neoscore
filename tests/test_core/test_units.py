import unittest

import pytest

from neoscore.core.units import Inch, Mm, Unit, make_unit_class
from tests.helpers import assert_almost_equal

MockUnit = make_unit_class("MockUnit", 2)


class TestUnit(unittest.TestCase):
    def test_init_from_int(self):
        unit = Unit(5)
        assert unit.base_value == 5

    def test_init_from_self_type(self):
        assert Unit(Unit(5)).base_value == 5

    def test_init_from_other_compatible_type(self):
        assert Unit(MockUnit(1)).base_value == 2

    def test_display_value(self):
        assert Unit(123.456).display_value == 123.456
        assert MockUnit(5).display_value == 5
        assert MockUnit(5).base_value == 10

    def test__repr__(self):
        assert repr(Unit(1)) == "Unit(1)"

    def test__lt__(self):
        assert Unit(1) < Unit(2)
        assert not Unit(1) < Unit(0)
        assert Unit(1) < MockUnit(1)
        assert not Unit(1) < MockUnit(0.5)
        with pytest.raises(AttributeError):
            Unit(1) < 5  # noqa

    def test__le__(self):
        assert Unit(1) <= Unit(2)
        assert Unit(1) <= Unit(1)
        assert not Unit(1) <= Unit(0)
        assert Unit(1) <= MockUnit(1)
        assert Unit(1) <= MockUnit(0.5)
        assert not Unit(1) <= MockUnit(0.4)
        with pytest.raises(AttributeError):
            Unit(1) <= 1  # noqa

    def test__eq__(self):
        assert Unit(1) == Unit(1)
        assert not Unit(1) == Unit(0)
        assert not Unit(1) == 1
        assert Unit(1) == MockUnit(0.5)
        assert not Unit(1) == MockUnit(1)

    def test__gt__(self):
        assert Unit(1) > Unit(0)
        assert not Unit(1) > Unit(2)
        assert not Unit(1) > Unit(1)
        assert Unit(1) > MockUnit(0.4)
        assert not Unit(1) > MockUnit(0.6)
        with pytest.raises(AttributeError):
            Unit(1) > 1  # noqa

    def test__ge__(self):
        assert Unit(1) >= Unit(0)
        assert Unit(1) >= Unit(1)
        assert not Unit(1) >= Unit(2)
        assert Unit(1) >= MockUnit(0.4)
        assert Unit(1) >= MockUnit(0.5)
        assert not Unit(1) >= MockUnit(0.6)
        with pytest.raises(AttributeError):
            Unit(1) >= 1  # noqa

    def test__add__(self):
        assert isinstance(Unit(1) + Unit(2), Unit)
        assert isinstance(Unit(1) + MockUnit(2), Unit)
        assert Unit(1) + Unit(2) == Unit(3)
        assert Unit(1) + MockUnit(2) == Unit(5)
        with pytest.raises(AttributeError):
            Unit(1) + 2  # noqa

    def test__sub__(self):
        assert isinstance(Unit(1) - Unit(2), Unit)
        assert isinstance(Unit(1) - MockUnit(2), Unit)
        assert Unit(1) - Unit(2) == Unit(-1)
        assert Unit(1) - MockUnit(2) == Unit(-3)
        with pytest.raises(AttributeError):
            Unit(1) + 2  # noqa

    def test__mul__(self):
        assert Unit(1) * 2 == Unit(2)
        with pytest.raises(TypeError):
            Unit(1) * Unit(1)  # noqa

    def test__rmul__(self):
        assert 2 * Unit(1) == Unit(2)

    def test__truediv__(self):
        assert Unit(1) / 2 == Unit(0.5)
        assert Unit(1) / MockUnit(1) == 0.5

    def test__pow__no_modulo(self):
        assert (Unit(2) ** 3) == Unit(8)
        with pytest.raises(TypeError):
            Unit(2) ** Unit(3)  # noqa

    def test__pow__with_modulo(self):
        assert (pow(Unit(2), 2, 3)).base_value == 1
        with pytest.raises(TypeError):
            # To use modulo, base value must be an int
            pow(Unit(2.3), 2, 1)  # noqa

    def test__neg__(self):
        assert -Unit(2) == Unit(-2)


class TestMm(unittest.TestCase):
    def test_mm_unit_conversion(self):
        assert_almost_equal(Mm(1), Unit(2.835), places=3)
        assert_almost_equal(Mm(2), Unit(5.669), places=3)


class TestInch(unittest.TestCase):
    def test_inch_unit_conversion(self):
        assert_almost_equal(Inch(1), Unit(72))
        assert_almost_equal(Inch(2), Unit(144))
