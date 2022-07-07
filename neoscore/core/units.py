"""Various interoperable units classes and some related helper functions."""
from __future__ import annotations

import decimal
from typing import Any, Optional, Type, TypeVar, Union, cast

TUnit = TypeVar("TUnit", bound="Unit")


class Unit:
    """An immutable graphical distance with a unit.

    Unit objects enable easy conversion from one unit to another and convenient
    operations between them.

    Common operators (``+``, ``-``, ``/``, etc.) are supported between them. Return
    values from these operations are given in the type on the left.

        >>> from neoscore.core.units import Inch, Mm
        >>> print(Inch(1) + Mm(1))
        Inch(1.039)

    To facilitate easy comparison between equivalent values in different units, equality
    is checked with a tolerance of ``Unit(0.001)``.

        >>> from neoscore.core.units import Inch, Mm
        >>> assert Inch(Mm(1)) == Mm(1)
        >>> assert Inch(Mm(1)) >= Mm(1)
        >>> assert Inch(Mm(1)) <= Mm(1)

    The base ``Unit`` type is a graphical unit corresponding to 1/72nd of an inch.
    Internally, this is significant because it is the unit used by the graphics backend,
    Qt. For most purposes, you probably want to use a more descriptive unit type.
    """

    __slots__ = {
        "base_value": "The underlying float value in base units.",
        "_display_value": "",
    }

    CONVERSION_RATE: float = 1
    """The ratio of this class to fundamental ``Unit``\ s.

    Subclasses should override this.
    """

    def __init__(self, value: Unit | float, _raw_base_value=None):
        """Create a unit from another unit or a raw number."""
        if _raw_base_value is not None:
            # Short-circuiting constructor for internal use
            self.base_value = _raw_base_value
            self._display_value = None
        else:
            base_value = getattr(value, "base_value", None)
            if base_value is not None:
                self.base_value = base_value
                self._display_value = None
            else:
                self.base_value = value * self.CONVERSION_RATE
                self._display_value = value

    @property
    def display_value(self) -> float:
        """A human-friendly unit value.

        If the unit was constructed with a simple number, this will return the exact
        given argument value. If the unit was constructed from another unit, this will
        return the converted value rounded to 3 decimal places.
        """
        if self._display_value:
            return self._display_value
        return round(self.base_value / self.CONVERSION_RATE, 3)

    @property
    def rounded_base_value(self) -> float:
        """The base value rounded to 2 decimal places.

        This is useful for things like hash keys for caching purposes
        """
        return round(self.base_value, 2)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.display_value)

    _CMP_POS_EPSILON = 0.001
    _CMP_NEG_EPSILON = -0.001

    def __lt__(self, other: Unit):
        return self.base_value - other.base_value < Unit._CMP_NEG_EPSILON

    def __le__(self, other: Unit):
        return self.base_value - other.base_value < Unit._CMP_POS_EPSILON

    def __eq__(self, other: Any):
        """Two units are equal if the difference between their base
        values is less than 0.001, or if both are infinite.
        """
        return hasattr(other, "base_value") and (
            # Check strict equality first for speed and coverage of infinity values
            self.base_value == other.base_value
            or abs(self.base_value - other.base_value) < Unit._CMP_POS_EPSILON
        )

    def __gt__(self, other: Unit):
        return self.base_value - other.base_value > Unit._CMP_POS_EPSILON

    def __ge__(self, other: Unit):
        return self.base_value - other.base_value > Unit._CMP_NEG_EPSILON

    def __add__(self: TUnit, other: TUnit) -> TUnit:
        return type(self)(None, _raw_base_value=self.base_value + other.base_value)

    def __sub__(self: TUnit, other: Unit) -> TUnit:
        return type(self)(None, _raw_base_value=self.base_value - other.base_value)

    def __mul__(self: TUnit, other: float) -> TUnit:
        if hasattr(other, "base_value"):
            raise TypeError
        return type(self)(None, _raw_base_value=self.base_value * other)

    def __rmul__(self: TUnit, other: float) -> TUnit:
        # __rmul__ behaves identically to __mul__
        if hasattr(other, "base_value"):
            raise TypeError
        return type(self)(None, _raw_base_value=self.base_value * other)

    def __truediv__(self: TUnit, other: Union[Unit, float]) -> Union[TUnit, float]:
        if hasattr(other, "base_value"):
            # Unit / Unit -> Float
            return self.base_value / (cast(Unit, other)).base_value
        # Unit / Float -> Unit
        return type(self)(None, _raw_base_value=self.base_value / other)

    def __pow__(self: TUnit, other: float, modulo: Optional[int] = None) -> TUnit:
        return type(self)(Unit(pow(self.base_value, other, modulo)))

    def __neg__(self: TUnit) -> TUnit:
        return type(self)(None, _raw_base_value=-self.base_value)

    def __abs__(self: TUnit) -> TUnit:
        return type(self)(None, _raw_base_value=abs(self.base_value))


class Inch(Unit):
    """An inch."""

    CONVERSION_RATE = 72


class Mm(Unit):
    """A millimeter."""

    CONVERSION_RATE = float(decimal.Decimal("0.0393700787") * Inch.CONVERSION_RATE)


ZERO = Unit(0)
"""Shorthand for a zero unit"""


def make_unit_class(name: str, conversion_rate: float) -> Type[Unit]:
    """Create a ``Unit`` subclass with a name and base unit conversion rate"""
    return cast(
        Type[Unit],
        type(
            name,
            (Unit,),
            {"CONVERSION_RATE": conversion_rate},
        ),
    )


def _convert_all_to_unit_out_of_place(
    collection: Union[tuple, set], unit: Type[Unit]
) -> Union[tuple, set]:
    mutable_iterable: List[Any] = list(collection)
    convert_all_to_unit(mutable_iterable, unit)
    return type(collection)(mutable_iterable)


def convert_all_to_unit(collection: Union[list, dict], unit: Type[Unit]):
    """Recursively convert all numbers found in a list or dict to a unit in place.

    This function works in place. Tuples and sets found within ``collection`` will be
    replaced.

    In dictionaries, only values are converted.
    """
    if isinstance(collection, dict):
        for key, value in collection.items():
            if isinstance(value, (int, float, Unit)):
                collection[key] = unit(value)
            elif isinstance(value, (list, dict)):
                convert_all_to_unit(collection[key], unit)
            elif isinstance(value, (tuple, set)):
                collection[key] = _convert_all_to_unit_out_of_place(
                    collection[key], unit
                )
            # (else: continue --- nothing to do here)
    elif isinstance(collection, list):
        for i in range(len(collection)):
            if isinstance(collection[i], (int, float, Unit)):
                collection[i] = unit(collection[i])
            elif isinstance(collection[i], (list, dict)):
                convert_all_to_unit(collection[i], unit)
            elif isinstance(collection[i], (tuple, set)):
                collection[i] = _convert_all_to_unit_out_of_place(collection[i], unit)
            # (else: continue --- nothing to do here)
    else:
        raise TypeError
