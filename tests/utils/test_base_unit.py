import pytest

from brown.utils.base_unit import BaseUnit


class MockUnit(BaseUnit):
    _base_units_per_self_unit = 2
    pass


def test_init_from_int():
    unit = BaseUnit(5)
    assert(isinstance(unit.value, int))
    assert(unit.value == 5)


def test_init_from_float():
    unit = BaseUnit(5.0)
    assert(isinstance(unit.value, float))
    assert(unit.value == 5.0)


def test_init_from_self_type():
    assert(BaseUnit(BaseUnit(5)).value == 5)


def test_init_from_other_compatible_type():
    assert(BaseUnit(MockUnit(1)).value == 2)


def test_init_from_incompatible_type_fails():
    with pytest.raises(TypeError):
        BaseUnit('nonsense type')


def test__str__():
    assert(str(BaseUnit(1)) == '1 base units')


def test__lt__():
    assert(BaseUnit(1) < BaseUnit(2))
    assert(not BaseUnit(1) < BaseUnit(0))
    assert(BaseUnit(1) < 5)
    assert(BaseUnit(1) < MockUnit(1))
    assert(not BaseUnit(1) < MockUnit(0.5))


def test__le__():
    assert(BaseUnit(1) <= BaseUnit(2))
    assert(BaseUnit(1) <= BaseUnit(1))
    assert(not BaseUnit(1) <= BaseUnit(0))
    assert(BaseUnit(1) <= 5)
    assert(BaseUnit(1) <= 1)
    assert(BaseUnit(1) <= MockUnit(1))
    assert(BaseUnit(1) <= MockUnit(0.5))
    assert(not BaseUnit(1) <= MockUnit(0.4))


def test__eq__():
    assert(BaseUnit(1) == BaseUnit(1))
    assert(not BaseUnit(1) == BaseUnit(0))
    assert(BaseUnit(1) == 1)
    assert(not BaseUnit(1) == 2)
    assert(BaseUnit(1) == MockUnit(0.5))
    assert(not BaseUnit(1) == MockUnit(1))


def test__ne__():
    assert(BaseUnit(1) != BaseUnit(2))
    assert(not BaseUnit(1) != BaseUnit(1))
    assert(BaseUnit(1) != MockUnit(1))
    assert(not BaseUnit(1) != MockUnit(0.5))
    assert(BaseUnit(1) != 2)
    assert(not BaseUnit(1) != 1)


def test__gt__():
    assert(BaseUnit(1) > BaseUnit(0))
    assert(not BaseUnit(1) > BaseUnit(2))
    assert(not BaseUnit(1) > BaseUnit(1))
    assert(BaseUnit(1) > 0)
    assert(not BaseUnit(1) > 2)
    assert(BaseUnit(1) > MockUnit(0.4))
    assert(not BaseUnit(1) > MockUnit(0.6))


def test__ge__():
    assert(BaseUnit(1) >= BaseUnit(0))
    assert(BaseUnit(1) >= BaseUnit(1))
    assert(not BaseUnit(1) >= BaseUnit(2))
    assert(BaseUnit(1) >= 0)
    assert(BaseUnit(1) >= 1)
    assert(not BaseUnit(1) >= 2)
    assert(BaseUnit(1) >= MockUnit(0.4))
    assert(BaseUnit(1) >= MockUnit(0.5))
    assert(not BaseUnit(1) >= MockUnit(0.6))


def test__add__():
    assert(isinstance(BaseUnit(1) + BaseUnit(2), BaseUnit))
    assert(isinstance(BaseUnit(1) + MockUnit(2), BaseUnit))
    assert((BaseUnit(1) + BaseUnit(2)).value == 3)
    assert((BaseUnit(1) + 2).value == 3)
    assert((BaseUnit(1) + MockUnit(1)).value == 3)


def test__sub__():
    assert(isinstance(BaseUnit(1) - BaseUnit(2), BaseUnit))
    assert(isinstance(BaseUnit(1) - MockUnit(2), BaseUnit))
    assert((BaseUnit(1) - BaseUnit(2)).value == -1)
    assert((BaseUnit(1) - 2).value == -1)
    assert((BaseUnit(1) - MockUnit(1)).value == -1)


def test__mul__():
    assert(isinstance(BaseUnit(1) * BaseUnit(2), BaseUnit))
    assert(isinstance(BaseUnit(1) * MockUnit(2), BaseUnit))
    assert((BaseUnit(1) * BaseUnit(2)).value == 2)
    assert((BaseUnit(1) * 2).value == 2)
    assert((BaseUnit(1) * MockUnit(1)).value == 2)


def test__truediv__():
    assert(isinstance(BaseUnit(1) / BaseUnit(2), BaseUnit))
    assert(isinstance(BaseUnit(1) / MockUnit(2), BaseUnit))
    assert((BaseUnit(1) / BaseUnit(2)).value == 0.5)
    assert((BaseUnit(1) / 2).value == 0.5)
    assert((BaseUnit(1) / MockUnit(1)).value == 0.5)


def test__floordiv__():
    assert(isinstance(BaseUnit(1) // BaseUnit(2), BaseUnit))
    assert(isinstance(BaseUnit(1) // MockUnit(2), BaseUnit))
    assert((BaseUnit(1) // BaseUnit(2)).value == 0)
    assert((BaseUnit(1) // 2).value == 0)
    assert((BaseUnit(1) // MockUnit(1)).value == 0)


def test__pow__no_modulo():
    assert(isinstance(BaseUnit(1) ** BaseUnit(2), BaseUnit))
    assert(isinstance(BaseUnit(1) ** MockUnit(2), BaseUnit))
    assert((BaseUnit(2) ** BaseUnit(2)).value == 4)
    assert((BaseUnit(2) ** 2).value == 4)
    assert((BaseUnit(2) ** MockUnit(1)).value == 4)


def test__pow__with_modulo():
    assert(isinstance(pow(BaseUnit(2), BaseUnit(2), 3), BaseUnit))
    assert(isinstance(pow(BaseUnit(2), MockUnit(2), 3), BaseUnit))
    assert((pow(BaseUnit(2), BaseUnit(2), 3)).value == 1)
    assert((pow(BaseUnit(2), 2, 3)).value == 1)
    assert((pow(BaseUnit(2), MockUnit(1), 3)).value == 1)


def test__int__():
    assert(isinstance(int(BaseUnit(2.0)), int))
    assert(int(BaseUnit(2.0)) == 2)


def test__float__():
    assert(isinstance(float(BaseUnit(2.0)), float))
    assert(float(BaseUnit(2.0)) == 2.0)


def test__round__():
    assert(isinstance(round(BaseUnit(2.21999)), BaseUnit))
    assert(round(BaseUnit(2.21999)).value == 2)
    assert(round(BaseUnit(2.21999), 1).value == 2.2)


def test__rmul__():
    assert(isinstance(1 * BaseUnit(2), BaseUnit))
    assert(isinstance(BaseUnit(2) * MockUnit(2), BaseUnit))
    assert((1 * BaseUnit(2)).value == BaseUnit(2))


def test__rtruediv__():
    assert(isinstance(1 / BaseUnit(2), BaseUnit))
    assert(isinstance(BaseUnit(1) / MockUnit(2), BaseUnit))
    assert((1 / BaseUnit(2)).value == BaseUnit(0.5))


def test__rfloordiv__():
    assert(isinstance(1 // BaseUnit(2), BaseUnit))
    assert(isinstance(BaseUnit(1) // MockUnit(2), BaseUnit))
    assert((1 // BaseUnit(2)).value == 0)
