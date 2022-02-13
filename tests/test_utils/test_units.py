import unittest

import pytest

from brown.utils.units import GraphicUnit, Inch, Mm, Unit, make_unit_class

MockUnit = make_unit_class("MockUnit", 2)


class TestUnit(unittest.TestCase):
    def test_init_from_int(self):
        unit = Unit(5)
        assert isinstance(unit.value, int)
        assert unit.value == 5

    def test_init_from_float(self):
        unit = Unit(5.0)
        assert isinstance(unit.value, float)
        assert unit.value == 5.0

    def test_init_from_self_type(self):
        assert Unit(Unit(5)).value == 5

    def test_init_from_other_compatible_type(self):
        assert Unit(MockUnit(1)).value == 2

    def test__repr__(self):
        assert repr(Unit(1)) == "Unit(1)"

    def test__hash__(self):
        assert hash(Unit(1)) == hash(MockUnit(0.5)) == 8726346
        assert len(set([Unit(1), MockUnit(0.5)])) == 1

    def test__lt__(self):
        assert Unit(1) < Unit(2)
        assert not Unit(1) < Unit(0)
        assert Unit(1) < MockUnit(1)
        assert not Unit(1) < MockUnit(0.5)
        with pytest.raises(AttributeError):
            Unit(1) < 5

    def test__le__(self):
        assert Unit(1) <= Unit(2)
        assert Unit(1) <= Unit(1)
        assert not Unit(1) <= Unit(0)
        assert Unit(1) <= MockUnit(1)
        assert Unit(1) <= MockUnit(0.5)
        assert not Unit(1) <= MockUnit(0.4)
        with pytest.raises(AttributeError):
            Unit(1) <= 1

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
            Unit(1) > 1

    def test__ge__(self):
        assert Unit(1) >= Unit(0)
        assert Unit(1) >= Unit(1)
        assert not Unit(1) >= Unit(2)
        assert Unit(1) >= MockUnit(0.4)
        assert Unit(1) >= MockUnit(0.5)
        assert not Unit(1) >= MockUnit(0.6)
        with pytest.raises(AttributeError):
            Unit(1) >= 1

    def test__add__(self):
        assert isinstance(Unit(1) + Unit(2), Unit)
        assert isinstance(Unit(1) + MockUnit(2), Unit)
        assert Unit(1) + Unit(2) == Unit(3)
        assert Unit(1) + MockUnit(2) == Unit(5)
        with pytest.raises(AttributeError):
            Unit(1) + 2

    def test__sub__(self):
        assert isinstance(Unit(1) - Unit(2), Unit)
        assert isinstance(Unit(1) - MockUnit(2), Unit)
        assert Unit(1) - Unit(2) == Unit(-1)
        assert Unit(1) - MockUnit(2) == Unit(-3)
        with pytest.raises(AttributeError):
            Unit(1) + 2

    def test__mul__(self):
        assert isinstance(Unit(1) * Unit(2), Unit)
        assert isinstance(Unit(1) * MockUnit(2), Unit)
        assert (Unit(1) * Unit(2)).value == 2
        assert (Unit(1) * 2).value == 2
        assert (Unit(1) * MockUnit(1)).value == 2

    def test__truediv__(self):
        assert Unit(1) / 2 == Unit(0.5)
        assert Unit(1) / MockUnit(1) == 0.5

    def test__pow__no_modulo(self):
        assert (Unit(2) ** 3) == Unit(8)
        with pytest.raises(TypeError):
            Unit(2) ** Unit(3)

    def test__pow__with_modulo(self):
        assert (pow(Unit(2), 2, 3)).value == 1
        with pytest.raises(TypeError):
            # To use modulo, base value must be an int
            pow(Unit(2.3), 2, 1)

    def test__neg__(self):
        assert -Unit(2) == Unit(-(2))

    def test__pos__(self):
        assert +Unit(-2) == Unit(+(-2))


class TestMm(unittest.TestCase):
    def test_mm_unit_conversion(self):
        self.assertAlmostEqual(Unit(Mm(1)), Unit(11.811029999999999))
        self.assertAlmostEqual(Unit(Mm(2)), Unit(23.622059999999998))


class TestInch(unittest.TestCase):
    def test_inch_unit_conversion(self):
        self.assertAlmostEqual(Unit(Inch(1)), Unit(300))
        self.assertAlmostEqual(Unit(Inch(2)), Unit(600))


class TestGraphicUnit(unittest.TestCase):
    def test_graphic_unit_unit_conversion(self):
        self.assertAlmostEqual(Unit(GraphicUnit(1)), Unit(1))
        self.assertAlmostEqual(Unit(GraphicUnit(2)), Unit(2))
