import pytest

from brown.utils.units import Unit


class MockUnit(Unit):
    _base_units_per_self_unit = 2
    pass


def test_init_from_int():
    unit = Unit(5)
    assert(isinstance(unit.value, int))
    assert(unit.value == 5)


def test_init_from_float():
    unit = Unit(5.0)
    assert(isinstance(unit.value, float))
    assert(unit.value == 5.0)


def test_init_from_self_type():
    assert(Unit(Unit(5)).value == 5)


def test_init_from_other_compatible_type():
    assert(Unit(MockUnit(1)).value == 2)


def test_init_from_incompatible_type_fails():
    with pytest.raises(TypeError):
        Unit('nonsense type')


def test__str__():
    assert(str(Unit(1)) == '1 base units')


def test__repr__():
    assert(repr(Unit(1)) == 'Unit(1)')


def test__lt__():
    assert(Unit(1) < Unit(2))
    assert(not Unit(1) < Unit(0))
    assert(Unit(1) < 5)
    assert(Unit(1) < MockUnit(1))
    assert(not Unit(1) < MockUnit(0.5))


def test__le__():
    assert(Unit(1) <= Unit(2))
    assert(Unit(1) <= Unit(1))
    assert(not Unit(1) <= Unit(0))
    assert(Unit(1) <= 5)
    assert(Unit(1) <= 1)
    assert(Unit(1) <= MockUnit(1))
    assert(Unit(1) <= MockUnit(0.5))
    assert(not Unit(1) <= MockUnit(0.4))


def test__eq__():
    assert(Unit(1) == Unit(1))
    assert(not Unit(1) == Unit(0))
    assert(Unit(1) == 1)
    assert(not Unit(1) == 2)
    assert(Unit(1) == MockUnit(0.5))
    assert(not Unit(1) == MockUnit(1))


def test__ne__():
    assert(Unit(1) != Unit(2))
    assert(not Unit(1) != Unit(1))
    assert(Unit(1) != MockUnit(1))
    assert(not Unit(1) != MockUnit(0.5))
    assert(Unit(1) != 2)
    assert(not Unit(1) != 1)


def test__gt__():
    assert(Unit(1) > Unit(0))
    assert(not Unit(1) > Unit(2))
    assert(not Unit(1) > Unit(1))
    assert(Unit(1) > 0)
    assert(not Unit(1) > 2)
    assert(Unit(1) > MockUnit(0.4))
    assert(not Unit(1) > MockUnit(0.6))


def test__ge__():
    assert(Unit(1) >= Unit(0))
    assert(Unit(1) >= Unit(1))
    assert(not Unit(1) >= Unit(2))
    assert(Unit(1) >= 0)
    assert(Unit(1) >= 1)
    assert(not Unit(1) >= 2)
    assert(Unit(1) >= MockUnit(0.4))
    assert(Unit(1) >= MockUnit(0.5))
    assert(not Unit(1) >= MockUnit(0.6))


def test__add__():
    assert(isinstance(Unit(1) + Unit(2), Unit))
    assert(isinstance(Unit(1) + MockUnit(2), Unit))
    assert((Unit(1) + Unit(2)).value == 3)
    assert((Unit(1) + 2).value == 3)
    assert((Unit(1) + MockUnit(1)).value == 3)


def test__sub__():
    assert(isinstance(Unit(1) - Unit(2), Unit))
    assert(isinstance(Unit(1) - MockUnit(2), Unit))
    assert((Unit(1) - Unit(2)).value == -1)
    assert((Unit(1) - 2).value == -1)
    assert((Unit(1) - MockUnit(1)).value == -1)


def test__mul__():
    assert(isinstance(Unit(1) * Unit(2), Unit))
    assert(isinstance(Unit(1) * MockUnit(2), Unit))
    assert((Unit(1) * Unit(2)).value == 2)
    assert((Unit(1) * 2).value == 2)
    assert((Unit(1) * MockUnit(1)).value == 2)


def test__truediv__():
    assert(isinstance(Unit(1) / Unit(2), Unit))
    assert(isinstance(Unit(1) / MockUnit(2), Unit))
    assert((Unit(1) / Unit(2)).value == 0.5)
    assert((Unit(1) / 2).value == 0.5)
    assert((Unit(1) / MockUnit(1)).value == 0.5)


def test__floordiv__():
    assert(isinstance(Unit(1) // Unit(2), Unit))
    assert(isinstance(Unit(1) // MockUnit(2), Unit))
    assert((Unit(1) // Unit(2)).value == 0)
    assert((Unit(1) // 2).value == 0)
    assert((Unit(1) // MockUnit(1)).value == 0)


def test__pow__no_modulo():
    assert(isinstance(Unit(1) ** Unit(2), Unit))
    assert(isinstance(Unit(1) ** MockUnit(2), Unit))
    assert((Unit(2) ** Unit(2)).value == 4)
    assert((Unit(2) ** 2).value == 4)
    assert((Unit(2) ** MockUnit(1)).value == 4)


def test__pow__with_modulo():
    assert(isinstance(pow(Unit(2), Unit(2), 3), Unit))
    assert(isinstance(pow(Unit(2), MockUnit(2), 3), Unit))
    assert((pow(Unit(2), Unit(2), 3)).value == 1)
    assert((pow(Unit(2), 2, 3)).value == 1)
    assert((pow(Unit(2), MockUnit(1), 3)).value == 1)


def test__int__():
    assert(isinstance(int(Unit(2.0)), int))
    assert(int(Unit(2.0)) == 2)


def test__float__():
    assert(isinstance(float(Unit(2.0)), float))
    assert(float(Unit(2.0)) == 2.0)


def test__round__():
    assert(isinstance(round(Unit(2.21999)), Unit))
    assert(round(Unit(2.21999)).value == 2)
    assert(round(Unit(2.21999), 1).value == 2.2)


def test__rmul__():
    assert(isinstance(1 * Unit(2), Unit))
    assert(isinstance(Unit(2) * MockUnit(2), Unit))
    assert((1 * Unit(2)).value == Unit(2))


def test__rtruediv__():
    assert(isinstance(1 / Unit(2), Unit))
    assert(isinstance(Unit(1) / MockUnit(2), Unit))
    assert((1 / Unit(2)).value == Unit(0.5))


def test__rfloordiv__():
    assert(isinstance(1 // Unit(2), Unit))
    assert(isinstance(Unit(1) // MockUnit(2), Unit))
    assert((1 // Unit(2)).value == 0)
